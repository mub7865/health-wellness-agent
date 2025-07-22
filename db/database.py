import sqlite3
import json
from datetime import datetime
from context import UserSessionContext

DB_PATH = "user_sessions.db"

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                uid INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                data TEXT NOT NULL,
                created_at TEXT,
                last_updated TEXT
            )
        """)

import os
import json
from dataclasses import asdict  # ✅ for dataclass

DB_FOLDER = "db"
SESSION_FILE = "session.json"

# db/database.py
import json

def save_session(context_wrapper):
    try:
        context = context_wrapper.context
        
        # ✅ Convert to dict manually
        data = {
            "name": getattr(context, "name", None),
            "uid": getattr(context, "uid", None),
            "goal": getattr(context, "goal", None),
            "diet_preferences": getattr(context, "diet_preferences", None),
            "workout_plan": getattr(context, "workout_plan", None),
            "meal_plan": getattr(context, "meal_plan", None),
            "injury_notes": getattr(context, "injury_notes", None),
            "handoff_logs": getattr(context, "handoff_logs", []),
            "progress_logs": getattr(context, "progress_logs", []),
            "last_user_message": getattr(context, "last_user_message", None)
        }

        with open("session.json", "w") as f:
            json.dump(data, f, indent=2)

        print("✅ Session saved to session.json")
    except Exception as e:
        print(f"❌ Failed to save session: {e}")

def load_session(uid: int) -> UserSessionContext | None:
    with sqlite3.connect(DB_PATH) as conn:
        row = conn.execute("SELECT data FROM sessions WHERE uid = ?", (uid,)).fetchone()
        if not row:
            return None
        return UserSessionContext(**json.loads(row[0]))
