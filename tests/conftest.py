from dotenv import load_dotenv
import pytest
import psycopg2
import os

load_dotenv()

@pytest.fixture(scope="session")
def db_connection():
    conn = psycopg2.connect(
        host=os.getenv("RDS_HOST"),
        port=os.getenv("RDS_PORT"),
        database=os.getenv("RDS_DATABASE"),
        user=os.getenv("RDS_USER"),
        password=os.getenv("RDS_PASSWORD"),
    )
    yield conn
    conn.close()

@pytest.fixture
def cursor(db_connection):
    """Create a cursor for each test."""
    cur = db_connection.cursor()
    yield cur
    cur.close()