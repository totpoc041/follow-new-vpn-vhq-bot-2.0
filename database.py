import json
import logging
import sqlite3
from datetime import datetime
from pathlib import Path

import config


DB_NAME = config.AppConfig.DATABASE_PATH


def _ensure_db_directory():
    db_path = Path(DB_NAME)
    if db_path.parent != Path("."):
        db_path.parent.mkdir(parents=True, exist_ok=True)

def init_db():
    _ensure_db_directory()
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE,
            uuid TEXT,
            profile TEXT,
            pos TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS admins (
            admin_id INTEGER PRIMARY KEY AUTOINCREMENT,
            tg_id INTEGER UNIQUE
        )
    """)
    conn.commit()
    conn.close()


def get_all_user_ids():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM users")
    users = cursor.fetchall()
    conn.close()
    return [user[0] for user in users]
    

def get_user(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user


def add_user(user_id, username, balance=0.0):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        profile = {
            "username": username,
            "date_reg": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "balance": balance,
            "ticket_tariff": None
        }
        profile_json = json.dumps(profile)
        cursor.execute("INSERT INTO users (user_id, profile) VALUES (?, ?)", (user_id, profile_json))
        conn.commit()


def update_user_uuid(user_id, uuid):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET uuid = ? WHERE user_id = ?", (uuid, user_id))
    conn.commit()
    conn.close()


def get_admins():
    """Получить список администраторов"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT tg_id FROM admins")
    admins = cursor.fetchall()
    conn.close()
    return [admin[0] for admin in admins]


def update_pos(new_pos, user_id):
    """Обновляет позицию (pos) пользователя в БД."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET pos = ? WHERE user_id = ?", (new_pos, user_id))
    conn.commit()
    conn.close()


def add_balance(user_id: int):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT profile FROM users WHERE user_id = ?", (user_id,))
    user = cursor.fetchone()
    if user:
        profile = json.loads(user[0])
        current_balance = profile.get('balance', 0)
        new_balance = current_balance + config.TariffConfig.TARIFFS["30day"]["price"]

        profile['balance'] = new_balance
        cursor.execute("UPDATE users SET profile = ? WHERE user_id = ?", (json.dumps(profile), user_id))
        conn.commit()
    conn.close()


def get_user_balance(user_id: int):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT profile FROM users WHERE user_id = ?", (user_id,))
    user = cursor.fetchone()

    if user:
        profile = json.loads(user[0])
        conn.close()
        return profile.get('balance', 0)
    conn.close()
    return 0


def update_balance(user_id, amount):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT profile FROM users WHERE user_id = ?", (user_id,))
    profile_json = cursor.fetchone()

    if profile_json:
        profile = json.loads(profile_json[0])
        profile['balance'] += amount
        cursor.execute("UPDATE users SET profile = ? WHERE user_id = ?", (json.dumps(profile), user_id))
        conn.commit()
    conn.close()


def update_user_profile(user_id, profile_data):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
            UPDATE users
            SET profile = ?
            WHERE user_id = ?
        """, (profile_data, user_id))
    conn.commit()
    conn.close()


def update_user_tariff(user_id, tariff):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT profile FROM users WHERE user_id = ?", (user_id,))
    profile_json = cursor.fetchone()

    if profile_json:
            profile = json.loads(profile_json[0])
            profile['ticket_tariff'] = tariff
            cursor.execute("UPDATE users SET profile = ? WHERE user_id = ?", (json.dumps(profile), user_id))
            conn.commit()
    conn.close()


def clear_user_tariff(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT profile FROM users WHERE user_id = ?", (user_id,))
    profile_json = cursor.fetchone()

    if profile_json:
        profile = json.loads(profile_json[0])
        profile.pop('ticket_tariff', None)
        cursor.execute("UPDATE users SET profile = ? WHERE user_id = ?", (json.dumps(profile), user_id))
        conn.commit()
    conn.close()


def get_user_profile(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT profile FROM users WHERE user_id = ?", (user_id,))
    profile_json = cursor.fetchone()

    if profile_json:
        profile = json.loads(profile_json[0])
        conn.close()
        return profile
    conn.close()
