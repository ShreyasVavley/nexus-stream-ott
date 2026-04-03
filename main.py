from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from db_manager import db_engine
import ott_logic

# Standard FastAPI server setup for Nexus Stream Platform.
app = FastAPI(title="Nexus Stream OTT API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Fine for local dev and testing.
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    # Setup tables and seed data for local testing.
    ott_logic.setup_database()
    ott_logic.seed_test_data()

@app.get("/")
def read_root():
    return {"status": "online", "platform": "Nexus Stream"}

@app.get("/trending")
def get_trending():
    # Fetch results from our SQL View
    rows = db_engine.run_query("SELECT * FROM v_trending LIMIT 5", fetch=True)
    return [{"id": r[0], "title": r[1], "views": r[2]} for r in rows]

@app.get("/users")
def get_users():
    # Basic user list for the dashboard.
    rows = db_engine.run_query("SELECT id, name, email FROM Users", fetch=True)
    return [{"id": r[0], "name": r[1], "email": r[2]} for r in rows]

@app.get("/play/{user_id}/{content_id}")
def stream_content(user_id: int, content_id: int):
    # Core subscription check logic.
    if ott_logic.can_user_watch(user_id):
        # Fetch the title. Direct SQL for speed.
        res = db_engine.run_query("SELECT title FROM Content WHERE id = ?", (content_id,), fetch=True)
        if not res:
            raise HTTPException(status_code=404, detail="Movie not found.")
        return {"status": "success", "message": f"Buffering '{res[0][0]}'... Enjoy your movie!"}
    
    # Generic access denied for non-active subscribers.
    raise HTTPException(status_code=403, detail="Subscription Expired. Peer-to-peer or local caching prevented.")
