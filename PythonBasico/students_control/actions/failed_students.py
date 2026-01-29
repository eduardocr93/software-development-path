def get_failed_subjects(student, passing_grade=60):
    failed = []

    if float(student["Spanish"]) < passing_grade:
        failed.append(("Spanish", student["Spanish"]))
    if float(student["English"]) < passing_grade:
        failed.append(("English", student["English"]))
    if float(student["Social Studies"]) < passing_grade:
        failed.append(("Social Studies", student["Social Studies"]))
    if float(student["Science"]) < passing_grade:
        failed.append(("Science", student["Science"]))

    return failed


def print_failed_student(student, failed_subjects):
    print(f"\nName: {student['Name']}")
    print(f"Class: {student['Class']}")
    print("Failed subjects:")
    for subject, grade in failed_subjects:
        print(f" - {subject} ({grade})")


def show_failed_students(students):
    if not students:
        print("No students in memory. Add or import first.")
        return

    print("\n===== FAILED STUDENTS =====")
    found = False

    for student in students:
        failed_subjects = get_failed_subjects(student)

        if failed_subjects:
            found = True
            print_failed_student(student, failed_subjects)

    if not found:
        print("No failed students!")
