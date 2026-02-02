def calculate_average(student):
    return (
        float(student["Spanish"]) +
        float(student["English"]) +
        float(student["Social Studies"]) +
        float(student["Science"])
    ) / 4


def show_top_3_students(students):

    if not students:
        print("No students in memory. Add or import first.")
        return

    sorted_students = sorted(students, key=calculate_average, reverse=True)
    top_3 = sorted_students[:3]

    print("\n===== TOP 3 STUDENTS =====")
    for i, student in enumerate(top_3, start=1):
        avg = calculate_average(student)
        print(f"\n#{i}")
        print(f"Name: {student['Name']}")
        print(f"Class: {student['Class']}")
        print(f"Average: {avg:.2f}")
