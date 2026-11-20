import tempfile
import unittest
from pathlib import Path

from taskflow import create_app


class DaymarkAppTestCase(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.app = create_app(
            {
                "TESTING": True,
                "DATABASE": str(Path(self.temp_dir.name) / "test.sqlite"),
                "SECRET_KEY": "test-key",
            }
        )
        self.client = self.app.test_client()

    def tearDown(self):
        self.temp_dir.cleanup()

    def create_task(self, title="Write project brief"):
        return self.client.post(
            "/tasks",
            data={
                "title": title,
                "notes": "A useful detail",
                "category": "Work",
                "priority": "High",
                "due_date": "",
            },
            follow_redirects=True,
        )

    def test_dashboard_renders_empty_state(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"A fresh start feels good.", response.data)

    def test_create_toggle_edit_and_delete_task(self):
        response = self.create_task()
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Write project brief", response.data)
        self.assertIn(b"0 of 1 complete", response.data)

    def test_invalid_task_is_not_saved(self):
        response = self.client.post(
            "/tasks", data={"title": "   "}, follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Add a task name before saving.", response.data)
        self.assertIn(b"A fresh start feels good.", response.data)

    def test_task_actions_and_validation(self):
        self.client.post(
            "/tasks",
            data={
                "title": "Write project brief",
                "category": "Work",
                "priority": "High",
                "due_date": "2026-11-21",
            },
        )
        task_page = self.client.get("/")
        self.assertIn(b"Nov 21", task_page.data)
        with self.app.app_context():
            from taskflow.db import get_db

            task_id = get_db().execute("SELECT id FROM tasks").fetchone()["id"]

        toggle = self.client.post(f"/tasks/{task_id}/toggle", follow_redirects=True)
        self.assertEqual(toggle.status_code, 200)
        self.assertIn(b"1 of 1 complete", toggle.data)

        edit = self.client.post(
            f"/tasks/{task_id}/edit",
            data={
                "title": "Revised project brief",
                "notes": "Updated details",
                "category": "Learning",
                "priority": "Low",
                "due_date": "",
            },
            follow_redirects=True,
        )
        self.assertIn(b"Revised project brief", edit.data)

        missing = self.client.get("/tasks/999")
        self.assertEqual(missing.status_code, 404)
        deleted = self.client.post(f"/tasks/{task_id}/delete", follow_redirects=True)
        self.assertEqual(deleted.status_code, 200)
        self.assertIn(b"A fresh start feels good.", deleted.data)


if __name__ == "__main__":
    unittest.main()
