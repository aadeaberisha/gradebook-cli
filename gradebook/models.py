from dataclasses import dataclass, field
from typing import List

def _require_non_empty_str(value: str, field_name: str) -> str:
    """Make sure the value is a non-empty string."""
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")
    return value.strip()

def _require_grade(grade: float) -> float:
    """Check that the grade is a number between 0 and 100 (returns rounded float)."""
    if not isinstance(grade, (int, float)):
        raise ValueError("grade must be a number.")
    g = float(grade)
    if g < 0 or g > 100:
        raise ValueError("grade must be between 0 and 100.")
    return round(g, 2)

@dataclass
class Student:
    """Student entity."""
    id: int
    name: str

    def __post_init__(self):
        self.name = _require_non_empty_str(self.name, "name")
        if not isinstance(self.id, int) or self.id <= 0:
            raise ValueError("id must be a positive integer.")

    def __str__(self) -> str:
        return f"Student(id={self.id}, name='{self.name}')"

@dataclass
class Course:
    """Course entity."""
    code: str
    title: str

    def __post_init__(self):
        self.code = _require_non_empty_str(self.code, "code")
        self.title = _require_non_empty_str(self.title, "title")

    def __str__(self) -> str:
        return f"Course(code='{self.code}', title='{self.title}')"

@dataclass
class Enrollment:
    """Enrollment connecting a student to a course, with a list of grades."""
    student_id: int
    course_code: str
    grades: List[float] = field(default_factory=list)

    def __post_init__(self):
        if not isinstance(self.student_id, int) or self.student_id <= 0:
            raise ValueError("student_id must be a positive integer.")
        self.course_code = _require_non_empty_str(self.course_code, "course_code")
        self.grades = [_require_grade(g) for g in self.grades]

    def add_grade(self, grade: float) -> None:
        """Add a new grade after checking it."""
        self.grades.append(_require_grade(grade))

    def __str__(self) -> str:
        return (
            f"Enrollment(student_id={self.student_id}, course_code='{self.course_code}', "
            f"grades={self.grades})"
        )
