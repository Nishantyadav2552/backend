# Project Documentation

## Overview
This project is a Python backend for bill/receipt extraction and monthly expense analysis. It is built with FastAPI and connects to Google Gemini for structured data extraction from OCR text.

The workspace root is `d:\bill_collector\backend`.

---

## Root Files

### `Dockerfile`
- Builds a container image from `python:3.11-slim-bookworm`.
- Sets working directory to `/srv`.
- Copies `requirements.txt` and installs dependencies.
- Copies the `app` directory into the container.
- Sets `WORKDIR /srv/app` and runs `uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}`.
- `PYTHONUNBUFFERED=1` ensures logs are printed immediately.

### `requirements.txt`
- Lists the runtime dependencies for the app:
  - `fastapi==0.115.0`
  - `uvicorn==0.30.6`
  - `google-generativeai==0.7.2`
  - `python-dotenv==1.0.1`

### `render.yaml`
- Describes the deployment configuration for Render or a similar PaaS.
- Configures a web service named `bill-collector-api`.
- Uses Python runtime.
- Build command: `pip install -r requirements.txt`.
- Start command: `cd app && uvicorn main:app --host 0.0.0.0 --port $PORT`.
- Sets `PYTHON_VERSION` to `3.11.9` and declares `ALLOWED_ORIGINS` as a runtime environment variable.

### `.gitignore`
- Excludes Python bytecode and common local environment artifacts:
  - `__pycache__/`
  - `*.py[cod]`
  - `.env`
  - virtual environment directories `.venv/` and `venv/`
  - image files `*.png`, `*.jpg`, `*.jpeg`

### `.dockerignore`
- Excludes build-time artifacts from Docker image context:
  - `.git`
  - `__pycache__`
  - `*.pyc`
  - local virtual environments `.venv`, `venv`
  - `.env`
  - `Bill.png`

### `.vscode/settings.json`
- Configures VS Code Python environment manager to use the system interpreter.

### `Bill.png`
- A root-level image asset not used by application code. Likely an example receipt or visual reference.

### `uploads/realistic-receipt-template_23-2147938550.avif`
- A static receipt image stored in the project uploads folder. This is likely a sample receipt template for testing or reference.

---

## Application Structure (`app/`)

### `app/main.py`
This is the FastAPI application entry point.

- Imports `FastAPI` and `CORSMiddleware`.
- Loads environment variables from `app/.env` using `dotenv` (via `gemini_extract.py`).
- Imports `extract_bill_with_gemini` from `services/gemini_extract`.
- Imports Pydantic request models `OCRRequest` and `MonthlyExpenseRequest`.
- Imports `generate_saving_suggestions` from `services.expense_advisor`.

#### Middleware
- Configures CORS origins from `ALLOWED_ORIGINS` environment variable.
- If `ALLOWED_ORIGINS` contains `*`, credentials are not explicitly allowed.
- Allows all methods and headers.

#### API Endpoints
- `GET /`
  - Returns a health-check JSON payload: `{"message": "Bill Extraction Backend Running"}`.

- `POST /extract-structured-data`
  - Accepts a JSON body matching `OCRRequest`.
  - Validates that `ocr_text` is present and non-empty.
  - Calls `extract_bill_with_gemini(ocr_text)` to generate structured receipt data.
  - Returns either `status: success` with `structured_data`, or `status: error` with a message.

- `POST /monthly-expense-analysis`
  - Accepts a JSON body matching `MonthlyExpenseRequest`.
  - Calls `generate_saving_suggestions(month, expenses)`.
  - Returns analysis results under `analysis`, or an error message.

---

## Models (`app/models`)

### `app/models/ocr_request.py`
- Defines `OCRRequest` with a single field:
  - `ocr_text: str`
- Used by `/extract-structured-data` to validate incoming OCR text.

### `app/models/monthly_expense_request.py`
- Defines the request schema for monthly expense analysis.

#### `ExpenseItem`
- `description: str`
- `total_amount: str`
- `date: str`
- `time: str`
- `ocr_text: str`

#### `MonthlyExpenseRequest`
- `month: str`
- `expenses: List[ExpenseItem]`

- Used by `/monthly-expense-analysis` to validate expense report input.

---

## Services (`app/services`)

### `app/services/gemini_extract.py`
This service is responsible for converting OCR text into structured receipt fields using Google Gemini.

- Loads environment variables from `app/.env`.
- Reads `GEMINI_API_KEY` and configures `google.generativeai` if available.
- Instantiates `model = genai.GenerativeModel("gemini-3-flash-preview")`.

#### `extract_bill_with_gemini(ocr_text)`
- Builds a prompt instructing Gemini to extract only these fields:
  1. `description`
  2. `total_amount`
  3. `date`
  4. `time`
- Requires valid JSON output, no explanation, and empty strings for missing fields.
- Sends the prompt to `model.generate_content(prompt)`.
- Cleans formatting markers like ````json`` and `````` from the response.
- Parses the cleaned text as JSON and returns it.
- On failure, returns an error object containing the exception message.

### `app/services/expense_advisor.py`
This service uses the same Gemini model instance imported from `gemini_extract.py` to generate advice.

#### `generate_saving_suggestions(month, expenses)`
- Builds a text representation of every expense item.
- Creates a prompt asking Gemini to:
  1. Provide a spending summary.
  2. Identify bad spending patterns.
  3. Offer savings suggestions.
  4. Estimate monthly savings.
- Requests valid JSON only with the structure:
  - `summary`
  - `bad_habits`
  - `suggestions`
  - `estimated_monthly_savings`
- Sends the prompt to `model.generate_content(prompt)`.
- Sanitizes the response text and parses JSON.
- Returns a JSON object or an error object on failure.

### `app/services/classify.py`
- Present in the service folder but currently empty.
- Its presence suggests intent for classification logic, but no implementation has been provided.

### `app/services/layoutlm.py`
- Present in the service folder but currently empty.
- Likely reserved for future LayoutLM-based OCR or document layout processing.

### `app/services/ner.py`
- Present in the service folder but currently empty.
- Likely reserved for future named entity recognition logic.

### `app/services/.gitignore`
- Contains `.env` to exclude service-level environment files from version control.

---

## Routes (`app/routes`)

### `app/routes/extract.py`
- File exists but is empty.
- Possibly intended to contain route definitions or extraction-related endpoint logic in the future.

---

## Directories

### `app/processed/`
- Present but empty.
- Likely intended for storing processed files or output artifacts.

### `app/uploads/`
- Directory exists and is empty.
- Likely intended for uploaded receipt files or temporary input files.

### `temp/`
- A root-level folder that currently appears as a placeholder.
- Often used for temporary data or intermediate files during processing.

### `uploads/`
- Contains a sample receipt asset:
  - `realistic-receipt-template_23-2147938550.avif`
- This image is likely used for testing OCR or as an example receipt.

---

## How the Project Works End-to-End

1. A client calls `POST /extract-structured-data` with JSON:
   ```json
   {"ocr_text": "..."}
   ```
2. `app/main.py` validates the request with `OCRRequest`.
3. `extract_bill_with_gemini` builds a Gemini prompt and requests structured JSON.
4. Gemini returns parsed fields which are returned as `structured_data`.

For monthly expense analysis:

1. A client calls `POST /monthly-expense-analysis` with JSON matching `MonthlyExpenseRequest`.
2. `app/main.py` validates the request.
3. `generate_saving_suggestions` creates a prompt summarizing all expenses.
4. Gemini returns JSON with savings advice and expense patterns.

The project is configured for deployment via Docker and Render, and it uses environment variables to configure allowed CORS origins and the Gemini API key.

---

## Important Environment Notes

- `GEMINI_API_KEY` must be set in `app/.env` or the runtime environment for Gemini requests to work.
- `ALLOWED_ORIGINS` can be set as a comma-separated list to control CORS.

---

## Summary of Empty or Placeholder Files

- `app/routes/extract.py`: empty route module.
- `app/services/classify.py`: empty service module.
- `app/services/layoutlm.py`: empty service module.
- `app/services/ner.py`: empty service module.
- `app/processed/`: empty directory.
- `app/uploads/`: empty directory.
- `temp/`: empty placeholder directory.

These appear to be scaffolding for future functionality.
