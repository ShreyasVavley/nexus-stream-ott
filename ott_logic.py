from db_manager import db_engine
import datetime

# --- OTT Platform Schema Definitions ---
def setup_database():
    # Make sure tables are there using a simple, readable SQL block.
    # No extra "Table" classes - just direct SQL hits as needed.
    schema_queries = [
        "CREATE TABLE IF NOT EXISTS Genres (id INTEGER PRIMARY KEY, name TEXT NOT NULL)",
        """CREATE TABLE IF NOT EXISTS Content (
            id INTEGER PRIMARY KEY, 
            title TEXT, 
            desc TEXT, 
            year INTEGER, 
            rating TEXT, 
            genre_id INTEGER, 
            FOREIGN KEY(genre_id) REFERENCES Genres(id))""",
        "CREATE TABLE IF NOT EXISTS Users (id INTEGER PRIMARY KEY, name TEXT, email UNIQUE, joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)",
        """CREATE TABLE IF NOT EXISTS Subscriptions (
            id INTEGER PRIMARY KEY, 
            user_id INTEGER, 
            plan TEXT, 
            status TEXT, 
            expiry DATE, 
            FOREIGN KEY(user_id) REFERENCES Users(id))""",
        """CREATE TABLE IF NOT EXISTS History (
            id INTEGER PRIMARY KEY, 
            user_id INTEGER, 
            content_id INTEGER, 
            watched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
            FOREIGN KEY(user_id) REFERENCES Users(id), 
            FOREIGN KEY(content_id) REFERENCES Content(id))"""
    ]
    for q in schema_queries:
        db_engine.run_query(q)

    # Simple Analytics View
    db_engine.run_query("DROP VIEW IF EXISTS v_trending")
    db_engine.run_query("""
        CREATE VIEW v_trending AS
        SELECT c.id, c.title, COUNT(h.id) as views
        FROM Content c
        JOIN History h ON c.id = h.content_id
        WHERE h.watched_at >= datetime('now', '-24 hours')
        GROUP BY c.id, c.title
        ORDER BY views DESC
    """)

# --- Core Business Logic ---

def can_user_watch(user_id):
    """Business rule: only users with Active subscription status can stream."""
    query = "SELECT status FROM Subscriptions WHERE user_id = ? AND status = 'Active'"
    res = db_engine.run_query(query, (user_id,), fetch=True)
    return len(res) > 0

def seed_test_data():
    # Only seed if no genres exist. Pure pragmatism.
    if db_engine.run_query("SELECT count(*) FROM Genres", fetch=True)[0][0] == 0:
        db_engine.run_query("INSERT INTO Genres (name) VALUES ('Sci-Fi'), ('Drama'), ('Action')")
        
        # Adding some movies
        movies = [
            ("Inception", 2010), ("Interstellar", 2014), ("The Matrix", 1999), 
            ("The Godfather", 1972), ("John Wick", 2014), ("Joker", 2019)
        ]
        for title, year in movies:
            db_engine.run_query("INSERT INTO Content (title, year, genre_id) VALUES (?, ?, 1)", (title, year))
        
        # Users & Subscriptions
        users = [("Dave", "dave@mail.com", "Active"), ("Sam", "sam@mail.com", "Expired")]
        for u_id, (name, email, status) in enumerate(users, 1):
            db_engine.run_query("INSERT INTO Users (name, email) VALUES (?,?)", (name, email))
            db_engine.run_query("INSERT INTO Subscriptions (user_id, plan, status) VALUES (?, 'Premium', ?)", (u_id, status))
        
        # Fake views in the last 24h
        for _ in range(5): db_engine.run_query("INSERT INTO History (user_id, content_id) VALUES (1, 1)")
        for _ in range(3): db_engine.run_query("INSERT INTO History (user_id, content_id) VALUES (1, 2)")
