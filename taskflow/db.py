import sqlite3
from pathlib import Path

from flask import current_app, g


def get_db():
    if "db" not in g:
        database_path = Path(current_app.config["DATABASE"])
        database_path.parent.mkdir(parents=True, exist_ok=True)
        g.db = sqlite3.connect(database_path)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


def close_db(_error=None):
    connection = g.pop("db", None)
    if connection is not None:
        connection.close()


def init_db(app):
    with app.app_context():
        get_db().executescript(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL CHECK(length(title) BETWEEN 1 AND 120),
                notes TEXT NOT NULL DEFAULT '' CHECK(length(notes) <= 500),
                category TEXT NOT NULL DEFAULT 'Personal'
                    CHECK(category IN ('Work', 'Personal', 'Health', 'Learning')),
                due_date TEXT,
                priority TEXT NOT NULL DEFAULT 'Medium'
                    CHECK(priority IN ('Low', 'Medium', 'High')),
                completed INTEGER NOT NULL DEFAULT 0 CHECK(completed IN (0, 1)),
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
            """
        )
        app.teardown_appcontext(close_db)
