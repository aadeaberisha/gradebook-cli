# GradeBook CLI

A simple **command-line GradeBook application** built with Python.  
It allows adding students, creating courses, enrolling them, assigning grades,  
and calculating averages or GPAs, with all data stored persistently in a JSON file.

---

##  Setup Instructions
### 1. Create and Activate a Virtual Environment & Clone the Repository

```bash
# Clone the repository
git clone https://github.com/aadeaberisha/gradebook-cli.git
cd gradebook

# Create a virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

---

### 2. Populate Sample Data
Before using the CLI, create sample data by running:
```bash
python -m scripts.seed
```

This command creates:
```bash
data/gradebook.json
```

---

### 4. Run the CLI Application
To start the GradeBook CLI, use:
```bash
python .\main.py
```

---

### 5. CLI Usage
Use the following commands:
```bash
# Add a new student
python .\main.py add-student --name "Adea"

# Add a new course
python .\main.py add-course --code WD101 --title "Web Development Basics"

# Enroll a student
python .\main.py enroll --student-id 1 --course WD101

# Add a grade for a student
python .\main.py add-grade --student-id 1 --course WD101 --grade 95

# List students, courses, or enrollments
python .\main.py list enrollments

# Compute average for a student’s course
python .\main.py avg --student-id 1 --course WD101

# Compute GPA for a student
python .\main.py gpa --student-id 1
```

---

### 6. Example CLI Workflow
Try this sequence of commands to test the full functionality:
```bash
python -m scripts.seed
python .\main.py list students
python .\main.py list courses
python .\main.py add-student --name "Leonora Mala"
python .\main.py enroll --student-id 4 --course PY101
python .\main.py add-grade --student-id 4 --course PY101 --grade 95
python .\main.py add-grade --student-id 4 --course PY101 --grade 88
python .\main.py list enrollments
python .\main.py avg --student-id 4 --course PY101
python .\main.py gpa --student-id 4
```

Expected Output:
```
Students:
  - id=1, name='Adea Berisha'
  - id=2, name='Liana Jusufi'
  - id=3, name='Erina Kelmendi'

Courses:
  - code='PY101', title='Python Programming Fundamentals'
  - code='DS201', title='Data Structures & Algorithms'
  - code='AI301', title='Introduction to Artificial Intelligence'

Student added: id=4, name='Leonora Mala'
Enrolled student 4 in PY101
Added grade 95 for student 4 in PY101
Added grade 88 for student 4 in PY101

Enrollments:
  - student_id=1, course='DS201', grades=[87]
  - student_id=1, course='PY101', grades=[96, 91]
  - student_id=3, course='DS201', grades=[78, 82]
  - student_id=4, course='PY101', grades=[95, 88]
  - student_id=2, course='AI301', grades=[90]
  - student_id=2, course='PY101', grades=[85]

Average for student 4 in PY101: 91.50
GPA for student 4: 91.50
```

---

### Logging
All application logs are automatically stored in:
```bash
logs/app.log
```

This includes INFO messages for normal operations and ERROR logs for exceptions.

---

### Unit Tests
Run all tests using:
```bash
python -m unittest -v tests/test_service.py
```

Expected output:
```
test_add_student_increments_id_and_stores_name ... ok
test_add_grade_happy_path ... ok
test_compute_average_happy_and_no_grades_edge ... ok

----------------------------------------------------------------------
Ran 3 tests in 0.007s

OK
```

---

### Design Decisions & Limitations
Design Choices

- Modular structure following PEP 8.

- Logging handled in utils.py.

- Data stored in a simple JSON file.

- CLI built using argparse with clear subcommands.

- Input validation with _require_non_empty_str() and _require_grade().

- Unit testing with Python’s unittest.

- Includes a sample data script (scripts/seed.py).

Limitations

- No duplicate student name check.

- GPA is a simple average.

- JSON file is single-user (not thread-safe).

- CLI only — no graphical interface.

---