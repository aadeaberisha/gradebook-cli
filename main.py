from __future__ import annotations
import argparse
import sys
from gradebook.utils import configure_logging
from gradebook import service


def _msg(e: Exception) -> str:
    """Return a clean error message without extra quotes for exceptions."""
    if getattr(e, "args", None):
        return str(e.args[0])
    return str(e)


def cmd_add_student(args: argparse.Namespace) -> None:
    """Handle the 'add-student' command to add a new student."""
    try:
        sid = service.add_student(args.name)
        print(f"Student added: id={sid}, name='{args.name}'")
    except Exception as e:
        print(f"Failed to add student: {_msg(e)}")


def cmd_add_course(args: argparse.Namespace) -> None:
    """Handle the 'add-course' command to add a new course."""
    try:
        code = args.code.upper()
        service.add_course(code, args.title)
        print(f"Course added: code='{code}', title='{args.title}'")
    except Exception as e:
        print(f"Failed to add course: {_msg(e)}")


def cmd_enroll(args: argparse.Namespace) -> None:
    """Handle the 'enroll' command to register a student in a course."""
    try:
        course = args.course.upper()
        service.enroll(args.student_id, course)
        print(f"Enrolled student {args.student_id} in {course}")
    except (KeyError, ValueError) as e:
        print(f"Enrollment error: {_msg(e)}")
    except Exception as e:
        print(f"Unexpected error: {_msg(e)}")


def cmd_add_grade(args: argparse.Namespace) -> None:
    """Handle the 'add-grade' command to assign a grade to a student."""
    try:
        course = args.course.upper()
        service.add_grade(args.student_id, course, args.grade)
        print(f"Added grade {args.grade} for student {args.student_id} in {course}")
    except (KeyError, ValueError) as e:
        print(f"Could not add grade: {_msg(e)}")
    except Exception as e:
        print(f"Unexpected error: {_msg(e)}")


def cmd_list(args: argparse.Namespace) -> None:
    """Handle the 'list' command to display students, courses, or enrollments."""
    try:
        if args.what == "students":
            items = service.list_students()
            if args.sort == "name":
                items = sorted(items, key=lambda s: s["name"].lower())
            print("Students:")
            for s in items:
                print(f"  - id={s['id']}, name='{s['name']}'")

        elif args.what == "courses":
            items = service.list_courses()
            if args.sort == "code":
                items = sorted(items, key=lambda c: c["code"].lower())
            print("Courses:")
            for c in items:
                print(f"  - code='{c['code']}', title='{c['title']}'")

        elif args.what == "enrollments":
            items = service.list_enrollments()
            print("Enrollments:")
            for e in items:
                print(f"  - student_id={e['student_id']}, course='{e['course_code']}', grades={e['grades']}")
        else:
            print("Unknown list target. Use: students | courses | enrollments")
    except Exception as e:
        print(f"Failed to list {args.what}: {_msg(e)}")


def cmd_avg(args: argparse.Namespace) -> None:
    """Handle the 'avg' command to compute a student's average in a course."""
    try:
        course = args.course.upper()
        avg = service.compute_average(args.student_id, course)
        print(f"Average for student {args.student_id} in {course}: {avg:.2f}")
    except (KeyError, ValueError) as e:
        print(f"Could not compute average: {_msg(e)}")
    except Exception as e:
        print(f"Unexpected error: {_msg(e)}")


def cmd_gpa(args: argparse.Namespace) -> None:
    """Handle the 'gpa' command to compute overall GPA for a student."""
    try:
        gpa = service.compute_gpa(args.student_id)
        print(f"GPA for student {args.student_id}: {gpa:.2f}")
    except (ValueError, KeyError) as e:
        print(f"Could not compute GPA: {_msg(e)}")
    except Exception as e:
        print(f"Unexpected error: {_msg(e)}")


def build_parser() -> argparse.ArgumentParser:
    """Build and return the argument parser with all CLI subcommands."""
    parser = argparse.ArgumentParser(prog="gradebook", description="Gradebook CLI")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_add_student = sub.add_parser("add-student", help="Add a student")
    p_add_student.add_argument("--name", required=True, help='Student name, e.g. "Alice"')
    p_add_student.set_defaults(func=cmd_add_student)

    p_add_course = sub.add_parser("add-course", help="Add a course")
    p_add_course.add_argument("--code", required=True, help="Course code, e.g. CS101")
    p_add_course.add_argument("--title", required=True, help='Course title, e.g. "Intro to CS"')
    p_add_course.set_defaults(func=cmd_add_course)

    p_enroll = sub.add_parser("enroll", help="Enroll a student into a course")
    p_enroll.add_argument("--student-id", type=int, required=True, help="Student id")
    p_enroll.add_argument("--course", required=True, help="Course code")
    p_enroll.set_defaults(func=cmd_enroll)

    p_add_grade = sub.add_parser("add-grade", help="Add a grade for a student's course")
    p_add_grade.add_argument("--student-id", type=int, required=True, help="Student id")
    p_add_grade.add_argument("--course", required=True, help="Course code")
    p_add_grade.add_argument("--grade", required=True, help="Grade value (0-100)")
    p_add_grade.set_defaults(func=cmd_add_grade)

    p_list = sub.add_parser("list", help="List entities")
    p_list.add_argument("what", choices=["students", "courses", "enrollments"], help="What to list")
    p_list.add_argument("--sort", choices=["name", "code"], help="Optional sort key")
    p_list.set_defaults(func=cmd_list)

    p_avg = sub.add_parser("avg", help="Compute average for one course")
    p_avg.add_argument("--student-id", type=int, required=True, help="Student id")
    p_avg.add_argument("--course", required=True, help="Course code")
    p_avg.set_defaults(func=cmd_avg)

    p_gpa = sub.add_parser("gpa", help="Compute GPA for a student")
    p_gpa.add_argument("--student-id", type=int, required=True, help="Student id")
    p_gpa.set_defaults(func=cmd_gpa)

    return parser


def main(argv: list[str] | None = None) -> int:
    """Main entry point for the Gradebook CLI."""
    try:
        configure_logging()
    except Exception:
        pass

    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)
    return 0


if __name__ == "__main__":
    sys.exit(main())
