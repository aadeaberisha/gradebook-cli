import unittest
from gradebook import service


class ServiceTests(unittest.TestCase):
    """Unit tests for Gradebook service layer functions."""

    def setUp(self):
        """Reset the in-memory database before each test."""
        service._db = {
            "students": [],
            "courses": [],
            "enrollments": [],
            "meta": {"next_student_id": 1},
        }

    def test_add_student_increments_id_and_stores_name(self):
        """Test that adding a student assigns a new ID and stores the name."""
        sid = service.add_student("Elira Dreshaj")
        self.assertEqual(sid, 1)
        self.assertEqual(service._db["students"][0]["name"], "Elira Dreshaj")

        sid2 = service.add_student("Ardit Kelmendi")
        self.assertEqual(sid2, 2)
        self.assertEqual(len(service._db["students"]), 2)

    def test_add_grade_happy_path(self):
        """Test adding a grade to an existing enrollment."""
        service._db = {
            "students": [{"id": 1, "name": "Elira Dreshaj"}],
            "courses": [{"code": "WD101", "title": "Web Development Basics"}],
            "enrollments": [{"student_id": 1, "course_code": "WD101", "grades": []}],
            "meta": {"next_student_id": 2},
        }

        service.add_grade(1, "WD101", 92)
        self.assertEqual(service._db["enrollments"][0]["grades"], [92])

    def test_compute_average_happy_and_no_grades_edge(self):
        """Test computing average and handle no-grade case."""
        service._db = {
            "students": [{"id": 1, "name": "Elira Dreshaj"}],
            "courses": [
                {"code": "DB201", "title": "Database Systems"},
                {"code": "AI301", "title": "Intro to Artificial Intelligence"},
            ],
            "enrollments": [
                {"student_id": 1, "course_code": "DB201", "grades": [85, 95]},
                {"student_id": 1, "course_code": "AI301", "grades": []},
            ],
            "meta": {"next_student_id": 2},
        }

        avg = service.compute_average(1, "DB201")
        self.assertEqual(avg, 90)

        with self.assertRaises(ValueError):
            service.compute_average(1, "AI301")


if __name__ == "__main__":
    unittest.main()
