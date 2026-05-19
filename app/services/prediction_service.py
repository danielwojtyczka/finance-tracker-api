from sqlalchemy.orm import Session
from app import models


def predict_next_month_expenses(db: Session):
    expenses = db.query(models.Expense).all()

    if not expenses:
        return {
            "predicted_month": "No data",
            "predicted_total": 0
        }

    monthly_totals = {}

    for expense in expenses:
        month = expense.date.strftime("%Y-%m")
        monthly_totals[month] = monthly_totals.get(month, 0) + expense.amount

    average_expenses = sum(monthly_totals.values()) / len(monthly_totals)

    return {
        "predicted_month": "next month",
        "predicted_total": round(average_expenses, 2)
    }