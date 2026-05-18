import json

from services.gemini_extract import model


def generate_saving_suggestions(
    month,
    expenses
):

    expense_text = ""

    for expense in expenses:

        expense_text += f"""
Description: {expense.description}
Amount: {expense.total_amount}
Date: {expense.date}
Time: {expense.time}

"""

    prompt = f"""
You are an AI financial advisor.

Analyze the following monthly expenses.

Provide:
1. Spending summary
2. Bad spending patterns
3. Suggestions to save money
4. Estimated monthly savings

Return ONLY valid JSON.

Format:

{{
  "summary": "",
  "bad_habits": [],
  "suggestions": [],
  "estimated_monthly_savings": ""
}}

MONTH:
{month}

EXPENSES:
{expense_text}
"""

    try:

        response = model.generate_content(
            prompt
        )

        response_text = response.text.strip()

        response_text = response_text.replace(
            "```json",
            ""
        ).replace(
            "```",
            ""
        ).strip()

        return json.loads(response_text)

    except Exception as e:

        return {
            "status": "error",
            "message": str(e)
        }