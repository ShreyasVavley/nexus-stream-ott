import sqlite3

# This is a simple wrapper around sqlite3 to make the main code cleaner.
# I'm using classic Python patterns here, nothing too fancy.

class DatabaseManager:
    def __init__(self, db_path="ott_platform.db"):
        self.db_path = db_path

    def connect(self):
        # Always return a new connection for simplicity with FastAPI if needed.
        return sqlite3.connect(self.db_path)

    def run_query(self, query, params=(), fetch=False):
        """Runs a SQL query and optionally returns the results."""
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            if fetch:
                return cursor.fetchall()
            conn.commit()

# I'll expose a global instance for easy use across the app.
db_engine = DatabaseManager()
