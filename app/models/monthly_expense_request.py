from pydantic import BaseModel
from typing import List


class ExpenseItem(BaseModel):

    description: str

    total_amount: str

    date: str

    time: str

    ocr_text: str


class MonthlyExpenseRequest(BaseModel):

    month: str

    expenses: List[ExpenseItem]