# AWS Glue ETL - Test Project

Pytest project for validating AWS Glue ETL outputs from two sources:
- S3 parquet data (via Pandas)
- PostgreSQL transformed table `shop.customer_orders_transformed` (via psycopg2)

## Project Structure

```
aws-glue-test-project/
├── tests/
│   ├── conftest.py         # Shared fixtures for RDS + S3
│   ├── rds/
│   │   └── test_rds.py     # SQL-based validation against transformed table
│   └── s3/
│       └── test_s3.py      # Dataframe-based validation for parquet data
├── .github/workflows/
│   └── test.yml            # GitHub Actions test workflow
├── refresh_aws_session.sh  # MFA helper for temporary AWS credentials
├── requirements.txt
├── .gitignore
└── readme.md
```

## What Is Tested

Both suites validate:
- **Schema**: expected columns and expected column count
- **Data quality**: row count, no NULL IDs
- **Transformations**: uppercase names and `total_amount = quantity * price`

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

3. Create a `.env` file in the project root:
```env
# RDS
RDS_HOST=your-rds-endpoint
RDS_PORT=5432
RDS_DATABASE=postgres
RDS_USER=postgres
RDS_PASSWORD=your_password

# S3 parquet path
S3_BUCKET=s3://your-bucket/path/to/file.parquet
```

## Run Tests

Run all tests:
```bash
pytest tests/ -v
```

Run only RDS tests:
```bash
pytest tests/rds/ -v
```

Run only S3 tests:
```bash
pytest tests/s3/ -v
```

Run with HTML report:
```bash
pip install pytest-html
pytest tests/ -v --html=report.html --self-contained-html
```

Then open `report.html` in your browser to view results.

## CI Notes

The GitHub Actions workflow currently runs the S3 suite (`tests/s3/`) on:
- push to `main` when files under `tests/**` change
- manual trigger (`workflow_dispatch`)

## Git Ignore Notes

Local runtime and editor artifacts are ignored, including:
- `.env`
- `venv/`
- `.pytest_cache/`
- `.cursor/`