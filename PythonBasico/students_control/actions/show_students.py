def show_students(students):

    if not students:
        print("No students in memory. Add or import first.")
        return

    print("\n===== STUDENT LIST =====")
    for i, student in enumerate(students, start=1):
        print(f"\nStudent {i}")
        print(f"Name: {student['Name']}")
        print(f"Class: {student['Class']}")
        print(f"Spanish: {student['Spanish']}")
        print(f"English: {student['English']}")
        print(f"Social Studies: {student['Social Studies']}")
        print(f"Science: {student['Science']}")
