# Finance Tracker API

Finance Tracker API is a backend REST API built with FastAPI and SQLAlchemy for managing personal expenses.

## Features

- Create expense
- Get all expenses
- Update expense
- Delete expense
- Import expenses from CSV
- Category summary report
- Monthly summary report
- Next month expense forecast

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- Uvicorn

## Run locally

Clone repository:

```bash
git clone https://github.com/danielwojtyczka/finance-tracker-api.git
cd finance-tracker-api
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run server:

```bash
uvicorn app.main:app --reload
```

Open Swagger docs:

```bash
http://127.0.0.1:8000/docs
```

## API Endpoints

- GET /expenses
- POST /expenses
- PUT /expenses/{id}
- DELETE /expenses/{id}
- POST /expenses/import-csv
- GET /report/category-summary
- GET /report/monthly-summary
- GET /prediction/next-month

## Testing

Run tests with:

```bash
pytest
```

Current test coverage:
- GET /expenses
- POST /expenses
- GET /prediction/next-month
