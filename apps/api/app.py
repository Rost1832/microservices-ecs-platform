import os
import time
import psycopg
from flask import Flask, jsonify, request

app = Flask(__name__)
DATABASE_URL = os.environ["DATABASE_URL"]

def get_conn():
    return psycopg.connect(DATABASE_URL)

def init_db():
    for attempt in range(10):
        try:
            with get_conn() as conn:
                conn.execute(
                    "CREATE TABLE IF NOT EXISTS items (id SERIAL PRIMARY KEY, name TEXT)"
                )
            print("DB ready, table ensured", flush=True)
            return
        except psycopg.OperationalError:
            print(f"DB not ready (attempt {attempt+1}), retrying...", flush=True)
            time.sleep(2)
    raise RuntimeError("Could not connect to the database")

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

@app.route("/api/items", methods=["GET"])
def get_items():
    with get_conn() as conn:
        rows = conn.execute("SELECT id, name FROM items ORDER BY id").fetchall()
    return jsonify([{"id": r[0], "name": r[1]} for r in rows])

@app.route("/api/items", methods=["POST"])
def create_item():
    data = request.get_json()
    name = data["name"]
    with get_conn() as conn:
        row = conn.execute(
            "INSERT INTO items (name) VALUES (%s) RETURNING id, name", (name,)
        ).fetchone()
    return jsonify({"id": row[0], "name": row[1]}), 201

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)