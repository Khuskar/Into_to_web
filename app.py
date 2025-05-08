import json
import sqlite3
from pathlib import Path
from flask import (
    Flask, render_template, request,
    redirect, url_for, jsonify, g, abort
)

app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
    SECRET_KEY="replace-me-in-prod",
    DATABASE=Path(app.instance_path) / "resume.db",
)
Path(app.instance_path).mkdir(parents=True, exist_ok=True)

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(
            app.config["DATABASE"],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(exc):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    db = get_db()
    db.executescript(
        """
        CREATE TABLE IF NOT EXISTS resume (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            data        TEXT NOT NULL,        -- full JSON blob
            created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
    )
    db.commit()


with app.app_context():
    init_db()

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/builder")
def builder():
    return render_template("resume.html")


@app.route("/save", methods=["POST"])
def save():

    try:
        payload = request.get_json(force=True)  # dict
    except Exception:
        abort(400, description="Invalid JSON")

    db = get_db()
    db.execute("INSERT INTO resume (data) VALUES (?)", (json.dumps(payload),))
    db.commit()
    return jsonify(status="ok"), 201

@app.route("/dashboard")
def dashboard():
    db = get_db()
    rows = db.execute(
        "SELECT id, created_at, data FROM resume ORDER BY created_at DESC"
    ).fetchall()
    return render_template("dashboard.html", resumes=rows)


@app.route("/resume/<int:resume_id>")
def resume_json(resume_id):
    db = get_db()
    row = db.execute(
        "SELECT data FROM resume WHERE id = ?", (resume_id,)
    ).fetchone()
    if row is None:
        abort(404, "Resume not found")
    return row["data"]



@app.route("/delete/<int:resume_id>", methods=["POST"])
def delete_resume(resume_id):
    db = get_db()
    db.execute("DELETE FROM resume WHERE id = ?", (resume_id,))
    db.commit()
    # small UX: redirect back to dashboard with a flash later if you want
    return redirect(url_for("dashboard"))


@app.route("/resumes")
def list_resumes():
    db = get_db()
    rows = db.execute(
        "SELECT id, created_at, data FROM resume ORDER BY created_at DESC"
    ).fetchall()
    return jsonify([
        {"id": r["id"], "created_at": r["created_at"], "data": json.loads(r["data"])}
        for r in rows
    ])

if __name__ == "__main__":
    app.run(debug=True)
