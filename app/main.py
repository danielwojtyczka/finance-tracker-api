import shutil
from typing import List

from app.services.prediction_service import predict_next_month_expenses
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session

from app.database import engine, Base, SessionLocal
from app import schemas, crud
from app.services.import_service import import_expenses_from_csv


app = FastAPI(title="Finance Tracker API")

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"message": "Finance Tracker API is running"}


@app.post("/expenses", response_model=schemas.ExpenseResponse)
def create_expense(
        expense: schemas.ExpenseCreate,
        db: Session = Depends(get_db)
):
    return crud.create_expense(db, expense)


@app.get("/expenses", response_model=List[schemas.ExpenseResponse])
def get_expenses(db: Session = Depends(get_db)):
    return crud.get_expenses(db)


@app.delete("/expenses/{expense_id}", response_model=schemas.ExpenseResponse)
def delete_expense(
        expense_id: int,
        db: Session = Depends(get_db)
):
    deleted_expense = crud.delete_expense(db, expense_id)

    if deleted_expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")

    return deleted_expense


@app.put("/expenses/{expense_id}", response_model=schemas.ExpenseResponse)
def update_expense(
        expense_id: int,
        updated_expense: schemas.ExpenseCreate,
        db: Session = Depends(get_db)
):
    expense = crud.update_expense(db, expense_id, updated_expense)

    if expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")

    return expense


@app.post("/expenses/import-csv", response_model=List[schemas.ExpenseResponse])
def import_csv(
        file: UploadFile = File(...),
        db: Session = Depends(get_db)
):
    file_path = f"temp_{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    imported_expenses = import_expenses_from_csv(db, file_path)

    return imported_expenses

@app.get("/report/category-summary", response_model=List[schemas.CategorySummary])
def category_summary(db: Session = Depends(get_db)):
    return crud.get_category_summary(db)

@app.get("/report/monthly-summary", response_model=List[schemas.MonthlySummary])
def monthly_summary(db: Session = Depends(get_db)):
    return crud.get_monthly_summary(db)

@app.get("/prediction/next-month", response_model=schemas.PredictionResponse)
def predict_next_month(db: Session = Depends(get_db)):
    return predict_next_month_expenses(db)