import pytest
import os
import pandas as pd

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

try:
    import psycopg2
except ImportError:
    pass


@pytest.fixture(scope="session")
def db_connection():
    conn = psycopg2.connect(
        host=os.getenv("RDS_HOST"),
        port=os.getenv("RDS_PORT"),
        database=os.getenv("RDS_DATABASE"),
        user=os.getenv("RDS_USER"),
        password=os.getenv("RDS_PASSWORD"),
    )
    try:
        yield conn
    finally:
        conn.close()


@pytest.fixture
def cursor(db_connection):
    cur = db_connection.cursor()
    yield cur
    cur.close()


@pytest.fixture
def df():
    return pd.read_parquet(
        os.getenv("S3_BUCKET"),
        storage_options={"anon": False},
    )