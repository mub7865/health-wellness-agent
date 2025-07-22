import sqlite3
import json
from datetime import datetime
from context import UserSessionContext
from typing import Optional

DB_PATH = "health_agent.db"

# --- DB Schema ---
# user_sessions: stores all main context fields
# handoff_logs: stores handoff log entries per user
# progress_logs: stores progress log entries per user

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_sessions (
            user_id INTEGER PRIMARY KEY,
            user_name TEXT,
            goal TEXT,
            diet_preferences TEXT,
            workout_plan TEXT,
            meal_plan TEXT,
            injury_notes TEXT,
            messages TEXT,
            last_interaction TIMESTAMP
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS handoff_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            log_entry TEXT,
            timestamp TIMESTAMP
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS progress_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            log_entry TEXT,
            timestamp TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


def save_user_session(context: UserSessionContext):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Serialize complex fields as JSON
    goal_json = json.dumps(context.goal) if context.goal else None
    workout_plan_json = json.dumps(context.workout_plan) if context.workout_plan else None
    meal_plan_json = json.dumps(context.meal_plan) if context.meal_plan else None
    messages_json = json.dumps(getattr(context, 'messages', []))
    # Upsert user session
    cursor.execute(
        """
        INSERT INTO user_sessions (user_id, user_name, goal, diet_preferences, workout_plan, meal_plan, injury_notes, messages, last_interaction)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(user_id) DO UPDATE SET
            user_name=excluded.user_name,
            goal=excluded.goal,
            diet_preferences=excluded.diet_preferences,
            workout_plan=excluded.workout_plan,
            meal_plan=excluded.meal_plan,
            injury_notes=excluded.injury_notes,
            messages=excluded.messages,
            last_interaction=excluded.last_interaction
        """,
        (
            context.uid,
            context.name,
            goal_json,
            context.diet_preferences,
            workout_plan_json,
            meal_plan_json,
            context.injury_notes,
            messages_json,
            datetime.now()
        )
    )
    # Save handoff logs
    for log in getattr(context, 'handoff_logs', []):
        cursor.execute(
            "INSERT INTO handoff_logs (user_id, log_entry, timestamp) VALUES (?, ?, ?)",
            (context.uid, log, datetime.now())
        )
    # Save progress logs
    for log in getattr(context, 'progress_logs', []):
        cursor.execute(
            "INSERT INTO progress_logs (user_id, log_entry, timestamp) VALUES (?, ?, ?)",
            (context.uid, json.dumps(log), datetime.now())
        )
    conn.commit()
    conn.close()


def load_user_session(user_id: int) -> Optional[UserSessionContext]:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_sessions WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return None
    (
        user_id, user_name, goal, diet_preferences, workout_plan,
        meal_plan, injury_notes, messages, last_interaction
    ) = row
    # Load handoff logs
    cursor.execute("SELECT log_entry FROM handoff_logs WHERE user_id = ?", (user_id,))
    handoff_logs = [r[0] for r in cursor.fetchall()]
    # Load progress logs
    cursor.execute("SELECT log_entry FROM progress_logs WHERE user_id = ?", (user_id,))
    progress_logs = [json.loads(r[0]) for r in cursor.fetchall()]
    conn.close()
    # Reconstruct context
    context = UserSessionContext(
        name=user_name,
        uid=user_id,
        goal=json.loads(goal) if goal else None,
        diet_preferences=diet_preferences,
        workout_plan=json.loads(workout_plan) if workout_plan else None,
        meal_plan=json.loads(meal_plan) if meal_plan else None,
        injury_notes=injury_notes,
        handoff_logs=handoff_logs,
        progress_logs=progress_logs
    )
    # Add messages if present
    if messages:
        context.messages = json.loads(messages)
    return context
