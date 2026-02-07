def get_failed_subjects(student, passing_grade=60):
    failed = []

    if student.spanish < passing_grade:
        failed.append(("Spanish", student.spanish))
    if student.english < passing_grade:
        failed.append(("English", student.english))
    if student.social_studies < passing_grade:
        failed.append(("Social Studies", student.social_studies))
    if student.science < passing_grade:
        failed.append(("Science", student.science))

    return failed


def print_failed_student(student, failed_subjects):
    print(f"\nName: {student.name}")
    print(f"Class: {student.student_class}")
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
