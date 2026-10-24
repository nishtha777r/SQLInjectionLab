
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import vulnerable_app as lab


class SQLInjectionLabTests(unittest.TestCase):

    def setUp(self):
        # Give each test its own temporary database.
        self.tempdir = tempfile.TemporaryDirectory()
        self.test_db = Path(self.tempdir.name) / "test_lab.db"

        self.db_patch = patch.object(lab, "DB_PATH", self.test_db)
        self.db_patch.start()

        lab.initialize_database()
        self.client = lab.app.test_client()

    def tearDown(self):
        self.db_patch.stop()
        self.tempdir.cleanup()

    def test_valid_secure_login(self):
        response = self.client.post(
            "/secure-login",
            data={
                "username": "admin",
                "password": "training-only-pass",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["status"], "success")

    def test_wrong_password_rejected(self):
        response = self.client.post(
            "/secure-login",
            data={
                "username": "admin",
                "password": "wrong-password",
            },
        )

        self.assertEqual(response.get_json()["status"], "failure")

    def test_vulnerable_route_demonstrates_lab_issue(self):
        response = self.client.post(
            "/login",
            data={
                "username": "admin' -- ",
                "password": "wrong-training-password",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["status"], "success")

    def test_secure_route_rejects_injection_input(self):
        response = self.client.post(
            "/secure-login",
            data={
                "username": "admin' -- ",
                "password": "wrong-training-password",
            },
        )

        self.assertEqual(response.status_code, 200)
        result = response.get_json()
        self.assertEqual(result["status"], "failure")
        self.assertEqual(result["rows"], [])

    def test_secure_page_loads(self):
        response = self.client.get("/secure")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Secure Login Training", response.data)


if __name__ == "__main__":
    unittest.main()
