import sqlite3
import os

DB_PATH = "bot_data.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Foydalanuvchilar jadvali
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id     INTEGER PRIMARY KEY,
            username    TEXT,
            full_name   TEXT,
            total_score INTEGER DEFAULT 0,
            games_played INTEGER DEFAULT 0,
            correct_answers INTEGER DEFAULT 0,
            joined_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # O'yin sessiyalari
    c.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            session_id  INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER,
            mode        TEXT,
            category    TEXT,
            score       INTEGER DEFAULT 0,
            total_q     INTEGER DEFAULT 0,
            correct     INTEGER DEFAULT 0,
            finished_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    """)

    # Reyting uchun oila guruhlari
    c.execute("""
        CREATE TABLE IF NOT EXISTS family_groups (
            group_id    INTEGER PRIMARY KEY,
            group_name  TEXT,
            total_score INTEGER DEFAULT 0,
            members     INTEGER DEFAULT 0,
            created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()

def get_or_create_user(user_id, username, full_name):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    user = c.fetchone()
    if not user:
        c.execute(
            "INSERT INTO users (user_id, username, full_name) VALUES (?,?,?)",
            (user_id, username, full_name)
        )
        conn.commit()
    conn.close()

def add_score(user_id, score, correct, total):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        UPDATE users SET
            total_score = total_score + ?,
            games_played = games_played + 1,
            correct_answers = correct_answers + ?
        WHERE user_id=?
    """, (score, correct, user_id))
    conn.commit()
    conn.close()

def get_top_users(limit=10):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        SELECT full_name, total_score, games_played, correct_answers
        FROM users ORDER BY total_score DESC LIMIT ?
    """, (limit,))
    rows = c.fetchall()
    conn.close()
    return rows

def get_user_stats(user_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    row = c.fetchone()
    conn.close()
    return row
