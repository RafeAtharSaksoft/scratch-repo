"""A new endpoint, added on a branch so there is a pull request to review.

Deliberately vulnerable, like app.py. Never deploy this.
"""
import sqlite3

from flask import request


def orders_for_customer():
    customer = request.args.get("customer_id", "")
    conn = sqlite3.connect("app.db")
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT id, total FROM orders WHERE customer_id = ?",
            (customer,),
        )
        rows = cur.fetchall()
        return {"orders": [{"id": row[0], "total": row[1]} for row in rows]}
    except Exception:
        return {"error": "An internal error occurred."}, 500
    finally:
        conn.close()


def order_note(order_id):
    conn = sqlite3.connect("app.db")
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT note FROM orders WHERE id = ?",
            (order_id,),
        )
        row = cur.fetchone()
        return row
    except Exception:
        return None
    finally:
        conn.close()
