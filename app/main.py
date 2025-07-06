from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)
DB_PATH = "penalties.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS penalties (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        player TEXT NOT NULL,
        reason TEXT NOT NULL,
        date TEXT NOT NULL
    )''')
    conn.commit()
    conn.close()

@app.route("/penalties", methods=["POST"])
def create_penalty():
    data = request.json
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO penalties (player, reason, date) VALUES (?, ?, ?)",
              (data["player"], data["reason"], data["date"]))
    conn.commit()
    conn.close()
    print(f"EVENT: penalty.created -> {data}")
    return jsonify({"message": "Penalty registered", "penalty": data}), 201

@app.route("/penalties", methods=["GET"])
def list_penalties():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, player, reason, date FROM penalties")
    rows = c.fetchall()
    conn.close()
    penalties = [{"id": r[0], "player": r[1], "reason": r[2], "date": r[3]} for r in rows]
    return jsonify(penalties)

if __name__ == "__main__":
    init_db()
    app.run(debug=True, host="0.0.0.0", port=5000)
