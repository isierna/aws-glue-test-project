# AWS Glue ETL - Test Project

Pytest project for validating the output of an AWS Glue ETL pipeline that joins customer data (RDS PostgreSQL) with order data (S3), transforms them, and writes results to `shop.customer_orders_transformed`.

## Project Structure

```
aws-glue-test-project/
├── tests/
│   ├── conftest.py              # Database connection fixtures
│   └── test_transformation.py   # Schema, data quality, and transformation tests
├── .env                         # Database credentials (not committed)
├── .gitignore
├── requirements.txt
└── README.md
```

## What's Tested

- **Schema**: table exists, correct column names, correct column count
- **Data Quality**: row count, no NULL primary keys
- **Transformations**: names are uppercase, total_amount = quantity × price, all customers joined

## Setup

1. Clone the repository:
```bash
git clone https://github.com/isierna/aws-glue-test-project.git
cd aws-glue-test-project
```

2. Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Create a `.env` file in the project root with your database credentials:
```
RDS_HOST=your-rds-endpoint
RDS_PORT=5432
RDS_DATABASE=postgres
RDS_USER=postgres
RDS_PASSWORD=your_password
```

## Run Tests

Run all tests:
```bash
pytest tests/ -v
```

Run with HTML report:
```bash
pip install pytest-html
pytest tests/ -v --html=report.html --self-contained-html
```

Then open `report.html` in your browser to view the results.