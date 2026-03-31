from dotenv import load_dotenv
import pytest
import psycopg2
import os
import pandas as pd
import json
import time

load_dotenv()

LOG_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    ".cursor",
    "debug-a376ec.log",
)
LOG_SESSION_ID = "a376ec"


def _agent_log(hypothesis_id, location, message, data=None, run_id="pre-debug"):
    """Append a single NDJSON debug line for offline inspection."""
    payload = {
        "sessionId": LOG_SESSION_ID,
        "runId": run_id,
        "hypothesisId": hypothesis_id,
        "location": location,
        "message": message,
        "data": data or {},
        "timestamp": int(time.time() * 1000),
    }
    os.makedirs(os.path.dirname(os.path.abspath(LOG_PATH)), exist_ok=True)
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(payload, ensure_ascii=True) + "\n")

@pytest.fixture(scope="session")
def db_connection():
    #region agent log
    _agent_log(
        "H1_dns_or_env",
        "tests/conftest.py:db_connection",
        "db_connection starting",
        data={
            "RDS_HOST": os.getenv("RDS_HOST"),
            "RDS_PORT": os.getenv("RDS_PORT"),
            "RDS_DATABASE": os.getenv("RDS_DATABASE"),
            "RDS_USER": os.getenv("RDS_USER"),
            "HTTP_PROXY": os.getenv("HTTP_PROXY") or os.getenv("http_proxy"),
            "HTTPS_PROXY": os.getenv("HTTPS_PROXY") or os.getenv("https_proxy"),
        },
    )
    #endregion

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

# RDS fixture
@pytest.fixture
def cursor(db_connection):
    """Create a cursor for each test."""
    cur = db_connection.cursor()
    yield cur
    cur.close()

# S3 fixture
@pytest.fixture
def df():
    #region agent log
    _agent_log(
        "H2_proxy_for_s3",
        "tests/conftest.py:df",
        "df fixture starting",
        data={
            "S3_BUCKET": os.getenv("S3_BUCKET"),
            "HTTP_PROXY": os.getenv("HTTP_PROXY") or os.getenv("http_proxy"),
            "HTTPS_PROXY": os.getenv("HTTPS_PROXY") or os.getenv("https_proxy"),
        },
    )
    #endregion

    try:
        return pd.read_parquet(
            os.getenv("S3_BUCKET"),
            storage_options={"anon": False},
        )
    except Exception as e:
        #region agent log
        _agent_log(
            "H2_proxy_for_s3",
            "tests/conftest.py:df",
            "df fixture failed",
            data={"error_type": type(e).__name__, "error": str(e)},
        )
        #endregion
        raise