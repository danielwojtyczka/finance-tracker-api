from datetime import date
from pydantic import BaseModel


class ExpenseCreate(BaseModel):
    title: str
    category: str
    amount: float
    date: date


class ExpenseResponse(ExpenseCreate):
    id: int

    class Config:
        from_attributes = True


class CategorySummary(BaseModel):
    category: str
    total: float


class MonthlySummary(BaseModel):
    month: str
    total: float


class PredictionResponse(BaseModel):
    predicted_month: str
    predicted_total: float