import sqlite3
from pathlib import Path
import json
from typing import Optional, List

DB_PATH = Path(__file__).parent.parent / "job_analyzer.db"


def get_db():
    """
    Creates/connects to SQLite database
    Returns a connection object
    """
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    """
    Creates the analyses table if it doesn't exist
    """
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS analyses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_description TEXT NOT NULL,
            company_name TEXT,
            result TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """
    )
    connection.commit()
    connection.close()


def save_analysis(jobDesc: str, companyName: str, result: dict) -> int:
    """
    Saves an analysis to the database
    Returns the ID of the inserted row
    """
    connection = get_db()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO analyses (job_description, company_name, result)
        VALUES (?, ?, ?)
        """,
        (jobDesc, companyName, json.dumps(result)),
    )

    insertedID = cursor.lastrowid
    connection.commit()
    connection.close()

    return insertedID


def get_analysis_by_id(id: int) -> Optional[dict]:
    """
    Fetches a single analysis by ID
    Returns None if not found
    """
    connection = get_db()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM analyses WHERE id = ?", (id,))
    row = cursor.fetchone()
    connection.close()

    if row is None:
        return None

    analysis = dict(row)
    analysis["result"] = json.loads(analysis["result"])

    return analysis


def get_all_analyses() -> List[dict]:
    """
    Fetches all analyses, most recent first.
    """
    connection = get_db()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM analyses ORDER BY created_at DESC")
    rows = cursor.fetchall()
    connection.close()

    analyses = [dict(row) for row in rows]
    for analysis in analyses:
        analysis["result"] = json.loads(analysis["result"])

    return analyses
