from sqlalchemy.orm import Session
from sqlalchemy import func
from app import models, schemas


def create_expense(db: Session, expense: schemas.ExpenseCreate):
    db_expense = models.Expense(
        title=expense.title,
        category=expense.category,
        amount=expense.amount,
        date=expense.date
    )

    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)

    return db_expense


def get_expenses(db: Session):
    return db.query(models.Expense).all()

def delete_expense(db: Session, expense_id: int):
    expense = db.query(models.Expense).filter(models.Expense.id == expense_id).first()

    if expense is None:
        return None

    db.delete(expense)
    db.commit()

    return expense

def update_expense(db: Session, expense_id: int, updated_expense: schemas.ExpenseCreate):
    expense = db.query(models.Expense).filter(models.Expense.id == expense_id).first()

    if expense is None:
        return None

    expense.title = updated_expense.title
    expense.category = updated_expense.category
    expense.amount = updated_expense.amount
    expense.date = updated_expense.date

    db.commit()
    db.refresh(expense)

    return expense

def get_category_summary(db: Session):
    return (
        db.query(
            models.Expense.category,
            func.sum(models.Expense.amount).label("total")
        )
        .group_by(models.Expense.category)
        .all()
    )

def get_monthly_summary(db: Session):
    expenses = db.query(models.Expense).all()

    monthly_totals = {}

    for expense in expenses:
        month = expense.date.strftime("%Y-%m")
        monthly_totals[month] = monthly_totals.get(month, 0) + expense.amount

    return [
        {"month": month, "total": total}
        for month, total in monthly_totals.items()
    ]