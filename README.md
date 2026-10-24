# SQLInjectionLab

A Python-based cybersecurity training project that demonstrates SQL injection vulnerabilities and shows how parameterized SQL queries help prevent them.

## Project Overview

SQLInjectionLab is a local web application built with Flask and SQLite. It contains an intentionally vulnerable login form, a secure login form, and a Python automation script for demonstrating SQL injection behavior against a dummy training database.

The project helps learners understand how unsafe SQL query construction can cause authentication bypasses and expose database schema information.

**This project is for educational use only. The vulnerable application must remain on localhost and must never be deployed publicly.**

## Features

- Local login form with an intentionally vulnerable SQL query.
- Secure login form using parameterized SQL queries.
- Dummy SQLite database with sample training accounts.
- Python automation script for testing the local lab.
- Demonstration of authentication bypass in the vulnerable route.
- Demonstration of database table-schema disclosure.
- Schema output saved to `schema_dump.txt`.
- Automated tests for vulnerable and secure login behavior.
- Runs locally on `127.0.0.1`.

## Technologies Used

- **Python 3**
- **Flask** for the local web application
- **SQLite** for the training database
- **urllib** for local HTTP requests
- **unittest** for automated testing

## Project Structure

```text
SQLInjectionLab/
├── vulnerable_app.py
├── sqli_lab.py
├── test_sql_injection_lab.py
├── README.md
├── .gitignore
├── lab.db
├── schema_dump.txt
└── .venv/
```

The database, schema dump, and virtual environment are generated or local-use files and should not be included in a public repository.

## Requirements

- Python 3
- Visual Studio Code or another Python editor
- Flask

## Installation

Open a terminal in the project directory.

Create a virtual environment:

```powershell
python -m venv .venv
```

Install Flask into that environment:

```powershell
.\.venv\Scripts\python.exe -m pip install Flask
```

These commands work in Windows PowerShell without requiring virtual-environment activation.

## Running the Application

Start the local Flask application:

```powershell
.\.venv\Scripts\python.exe vulnerable_app.py
```

Open the vulnerable training page:

http://127.0.0.1:5000/

Open the secure login page:

http://127.0.0.1:5000/secure

Keep the server terminal open while testing the application.

## Running the Automation Script

Open a second terminal in the project folder and run:

```powershell
.\.venv\Scripts\python.exe sqli_lab.py
```

The script sends requests to the fixed local endpoint and demonstrates login-bypass behavior and schema disclosure using the dummy SQLite database.

The resulting schema information is saved to `schema_dump.txt`.

## Running Automated Tests

Run the test suite using:

```powershell
.\.venv\Scripts\python.exe -m unittest -v test_sql_injection_lab.py
```

The tests cover:

- Successful login with valid dummy credentials.
- Rejection of an incorrect password.
- Login-bypass behavior in the intentionally vulnerable route.
- Rejection of the same injection input by the secure route.
- Successful loading of the secure login page.

A passing test suite should end with `OK`.

## Security Lessons

### Vulnerable SQL

The vulnerable route directly combines user input with an SQL statement. This allows crafted input to change the intended meaning of the query.

### Parameterized SQL

The secure route uses SQL placeholders and passes the username and password as separate values. This prevents user-supplied text from being interpreted as SQL instructions.

### Database Schema Disclosure

The training automation script demonstrates how an unsafe query can expose database table definitions.

## Limitations

- This is a deliberately vulnerable educational application, not a production authentication system.
- The training accounts use dummy plaintext passwords for demonstration.
- The application does not implement production-grade password hashing, session management, or account protection.
- The local lab is bound to `127.0.0.1` and should remain accessible only on the local computer.

## Responsible Use

Use this project only in your own isolated training environment with dummy data. Do not deploy the vulnerable route publicly or use the techniques against systems without explicit authorization.

## Author

Developed as a cybersecurity internship project to practise Python, SQL injection concepts, database security, and automated testing.