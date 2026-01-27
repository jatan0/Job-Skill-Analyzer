import sqlite3
from pathlib import Path

# Where to store the database file
DB_PATH = Path(__file__).parent.parent / "job_analyzer.db"


def get_db():
    """
    Creates/connects to SQLite database.
    Returns a connection object.
    """
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    """
    Creates the analyses table if it doesn't exist.
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


# if __name__ == "__main__":
#     print("Initializing database...")
#     init_db()
#     print("Database initialized!")

#     # Test that it worked
#     conn = get_db()
#     cursor = conn.cursor()
#     cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
#     tables = cursor.fetchall()
#     print(f"Tables in database: {[table['name'] for table in tables]}")
#     conn.close()
