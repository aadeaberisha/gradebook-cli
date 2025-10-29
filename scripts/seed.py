from gradebook import service
from gradebook.storage import save_data

def run_seed():
    """Create sample data for the Gradebook CLI (students, courses, enrollments, grades)."""

    service._db = {
        "students": [],
        "courses": [],
        "enrollments": [],
        "meta": {"next_student_id": 1},
    }

    sid1 = service.add_student("Adea Berisha")
    sid2 = service.add_student("Liana Jusufi")
    sid3 = service.add_student("Erina Kelmendi")

    service.add_course("PY101", "Python Programming Fundamentals")
    service.add_course("DS201", "Data Structures & Algorithms")
    service.add_course("AI301", "Introduction to Artificial Intelligence")

    service.enroll(sid1, "PY101")
    service.enroll(sid1, "DS201")
    service.enroll(sid2, "PY101")
    service.enroll(sid2, "AI301")
    service.enroll(sid3, "DS201")

    service.add_grade(sid1, "PY101", 96)
    service.add_grade(sid1, "PY101", 91)
    service.add_grade(sid1, "DS201", 87)

    service.add_grade(sid2, "PY101", 85)
    service.add_grade(sid2, "AI301", 90)

    service.add_grade(sid3, "DS201", 78)
    service.add_grade(sid3, "DS201", 82)

    save_data(service._db)
    print("Sample data seeded successfully! Database saved to data/gradebook.json")


if __name__ == "__main__":
    run_seed()
