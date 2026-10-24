
import sqlite3
from pathlib import Path
from contextlib import closing

from flask import Flask, jsonify, render_template_string, request

app = Flask(__name__)
DB_PATH = Path(__file__).with_name("lab.db")


LOGIN_PAGE = """
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>SQL Injection Training Lab</title>
</head>
<body>
    <h1>SQL Injection Training Lab</h1>
    <p>Local educational lab using dummy training accounts.</p>

    <form action="/login" method="post">
        <label>
            Username:
            <input name="username" required>
        </label>
        <br><br>
        <label>
            Password:
            <input name="password" type="password" required>
        </label>
        <br><br>
        <button type="submit">Test Login</button>
    </form>

    <p><a href="/secure">Open the secure login demonstration</a></p>
</body>
</html>
"""


SECURE_LOGIN_PAGE = """
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>Secure Login Training</title>
</head>
<body>
    <h1>Secure Login Training</h1>
    <p>This form uses parameterized SQL queries.</p>

    <form action="/secure-login" method="post">
        <label>
            Username:
            <input name="username" required>
        </label>
        <br><br>
        <label>
            Password:
            <input name="password" type="password" required>
        </label>
        <br><br>
        <button type="submit">Test Secure Login</button>
    </form>

    <p><a href="/">Return to vulnerable training page</a></p>
</body>
</html>
"""


def initialize_database():
    """Create the local database with fake training accounts."""
    with closing(sqlite3.connect(DB_PATH)) as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                role TEXT NOT NULL
            )
        """)

        connection.execute("""
            CREATE TABLE IF NOT EXISTS lab_notes (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                content TEXT NOT NULL
            )
        """)

        count = connection.execute(
            "SELECT COUNT(*) FROM users"
        ).fetchone()[0]

        if count == 0:
            connection.executemany(
                """
                INSERT INTO users (username, password, role)
                VALUES (?, ?, ?)
                """,
                [
                    ("admin", "training-only-pass", "admin"),
                    ("alice", "demo-only-pass", "user"),
                ],
            )

        count = connection.execute(
            "SELECT COUNT(*) FROM lab_notes"
        ).fetchone()[0]

        if count == 0:
            connection.execute(
                """
                INSERT INTO lab_notes (title, content)
                VALUES (?, ?)
                """,
                (
                    "Training note",
                    "Fake data for the local SQL injection lab only",
                ),
            )

        # Save database creation and inserted training records.
        connection.commit()


@app.route("/", methods=["GET"])
def index():
    return render_template_string(LOGIN_PAGE)


@app.route("/login", methods=["POST"])
def login():
    """Intentionally vulnerable route for local lab practice."""
    username = request.form.get("username", "")
    password = request.form.get("password", "")

    # INTENTIONALLY VULNERABLE:
    # User input is directly combined with the SQL statement.
    query = (
        "SELECT username, role FROM users "
        f"WHERE username = '{username}' "
        f"AND password = '{password}'"
    )

    try:
        with closing(sqlite3.connect(DB_PATH)) as connection:
            connection.row_factory = sqlite3.Row
            rows = [
                dict(row)
                for row in connection.execute(query).fetchall()
            ]

        return jsonify({
            "status": "success" if rows else "failure",
            "rows": rows,
        })

    except sqlite3.Error:
        return jsonify({
            "status": "error",
            "rows": [],
        }), 400


@app.route("/secure", methods=["GET"])
def secure_index():
    return render_template_string(SECURE_LOGIN_PAGE)


@app.route("/secure-login", methods=["POST"])
def secure_login():
    """Secure demonstration using parameterized SQL."""
    username = request.form.get("username", "")
    password = request.form.get("password", "")

    # SAFE: Input values are passed separately from SQL instructions.
    query = """
        SELECT username, role
        FROM users
        WHERE username = ? AND password = ?
    """

    try:
        with closing(sqlite3.connect(DB_PATH)) as connection:
            connection.row_factory = sqlite3.Row
            rows = [
                dict(row)
                for row in connection.execute(
                    query, (username, password)
                ).fetchall()
            ]

        return jsonify({
            "status": "success" if rows else "failure",
            "rows": rows,
        })

    except sqlite3.Error:
        return jsonify({
            "status": "error",
            "rows": [],
        }), 400


if __name__ == "__main__":
    initialize_database()

    # Keep the training application accessible only on this computer.
    app.run(host="127.0.0.1", port=5000, debug=False)
