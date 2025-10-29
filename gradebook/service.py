from __future__ import annotations
from typing import Dict, Any, List
from .models import Student, Course, Enrollment
from .storage import load_data, save_data
from .utils import parse_grade

_db, _path = load_data()
_db.setdefault("students", [])
_db.setdefault("courses", [])
_db.setdefault("enrollments", [])
_db.setdefault("meta", {"next_student_id": 1})

def _next_id() -> int:
    nid = _db["meta"].get("next_student_id", 1)
    _db["meta"]["next_student_id"] = nid + 1
    return nid

def add_student(name: str) -> int:
    """Add a student and return new id."""
    sid = _next_id()
    s = Student(id=sid, name=name)
    _db["students"].append({"id": s.id, "name": s.name})
    save_data(_db, _path)
    return sid

def add_course(code: str, title: str) -> None:
    """Add a course (error if code exists)."""
    if any(c["code"] == code for c in _db["courses"]):
        raise ValueError(f"Course '{code}' already exists.")
    c = Course(code=code, title=title)
    _db["courses"].append({"code": c.code, "title": c.title})
    save_data(_db, _path)

def enroll(student_id: int, course_code: str) -> None:
    """Enroll a student in a course."""
    if not any(s["id"] == student_id for s in _db["students"]):
        raise KeyError(f"No student with id {student_id}.")
    if not any(c["code"] == course_code for c in _db["courses"]):
        raise KeyError(f"No course with code '{course_code}'.")
    if any(e["student_id"] == student_id and e["course_code"] == course_code
           for e in _db["enrollments"]):
        return
    e = Enrollment(student_id=student_id, course_code=course_code)
    _db["enrollments"].append(
        {"student_id": e.student_id, "course_code": e.course_code, "grades": e.grades}
    )
    save_data(_db, _path)

def add_grade(student_id: int, course_code: str, grade: int) -> None:
    """Add a grade for a student's course."""
    g = parse_grade(grade)
    for e in _db["enrollments"]:
        if e["student_id"] == student_id and e["course_code"] == course_code:
            e["grades"].append(g)
            save_data(_db, _path)
            return
    raise KeyError(f"Student {student_id} not enrolled in '{course_code}'.")

def list_students() -> List[Dict[str, Any]]:
    """List students sorted by name."""
    return sorted(_db["students"], key=lambda s: s["name"].lower())

def list_courses() -> List[Dict[str, Any]]:
    """List courses sorted by code."""
    return sorted(_db["courses"], key=lambda c: c["code"].lower())

def list_enrollments() -> List[Dict[str, Any]]:
    """List enrollments sorted by student name then course code."""
    names = {s["id"]: s["name"] for s in _db["students"]}
    return sorted(
        _db["enrollments"],
        key=lambda e: (names.get(e["student_id"], "").lower(), e["course_code"].lower()),
    )

def compute_average(student_id: int, course_code: str) -> float:
    """Compute average grade for one course."""
    for e in _db["enrollments"]:
        if e["student_id"] == student_id and e["course_code"] == course_code:
            if not e["grades"]:
                raise ValueError("No grades for this student/course.")
            return sum(e["grades"]) / len(e["grades"])
    raise KeyError(f"Student {student_id} not enrolled in '{course_code}'.")

def compute_gpa(student_id: int) -> float:
    """Compute GPA (mean of course averages)."""
    avgs = [
        sum(e["grades"]) / len(e["grades"])
        for e in _db["enrollments"]
        if e["student_id"] == student_id and e["grades"]
    ]
    if not avgs:
        raise ValueError("No graded courses.")
    return sum(avgs) / len(avgs)
