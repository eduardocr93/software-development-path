from data.read_students import load_students_from_csv

def show_students():
    students = load_students_from_csv()

    if not students:
        print("No students found.")
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
