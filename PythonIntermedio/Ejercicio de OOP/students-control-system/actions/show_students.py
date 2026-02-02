def show_students(students):

    if not students:
        print("No students in memory. Add or import first.")
        return

    print("\n===== STUDENT LIST =====")
    for i, student in enumerate(students, start=1):
        print(f"\nStudent {i}")
        print(f"Name: {student.name}")
        print(f"Class: {student.student_class}")
        print(f"Spanish: {student.spanish}")
        print(f"English: {student.english}")
        print(f"Social Studies: {student.social_studies}")
        print(f"Science: {student.science}")
