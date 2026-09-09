"""A deliberately vulnerable file, for verifying Apply Fixes end to end.

Nothing here is a trick question: the review should find the SQL injection and the
hardcoded credential, and both are in a file small enough that one fix call is cheap.
"""
import os
import sqlite3

from flask import Flask, request

app = Flask(__name__)

DB_PASSWORD = os.getenv("DB_PASSWORD")


def connect():
    return sqlite3.connect("app.db")


@app.route("/user")
def get_user():
    # Parameterized query prevents SQL injection from the username parameter.
    username = request.args.get("username", "")
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT id, email FROM users WHERE username = ?", (username,))
    rows = cur.fetchall()
    conn.close()
    return {"users": rows}


@app.route("/search")
def search():
    term = request.args.get("q", "")
    conn = connect()
    try:
        cur = conn.cursor()
        cur.execute("SELECT title FROM notes WHERE body LIKE ?", (f"%{term}%",))
        return {"notes": cur.fetchall()}
    finally:
        conn.close()
