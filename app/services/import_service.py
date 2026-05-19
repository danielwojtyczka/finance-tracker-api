import pandas as pd
from sqlalchemy.orm import Session

from app import models


def import_expenses_from_csv(db: Session, file_path: str):
    data = pd.read_csv(file_path)

    imported_expenses = []

    for _, row in data.iterrows():
        expense = models.Expense(
            title=row["title"],
            category=row["category"],
            amount=float(row["amount"]),
            date=pd.to_datetime(row["date"]).date()
        )

        db.add(expense)
        imported_expenses.append(expense)

    db.commit()

    for expense in imported_expenses:
        db.refresh(expense)

    return imported_expenses