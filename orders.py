"""A new endpoint, added on a branch so there is a pull request to review.

Deliberately vulnerable, like app.py. Never deploy this.
"""
import sqlite3

from flask import request


def orders_for_customer():
    # SQL injection: the customer id is concatenated into the query.
    customer = request.args.get("customer_id", "")
    conn = sqlite3.connect("app.db")
    cur = conn.cursor()
    cur.execute("SELECT id, total FROM orders WHERE customer_id = " + customer)
    return {"orders": cur.fetchall()}


def order_note(order_id):
    conn = sqlite3.connect("app.db")
    cur = conn.cursor()
    cur.execute("SELECT note FROM orders WHERE id = '%s'" % order_id)
    return cur.fetchone()
