from data.read_students import load_students_from_csv


def calculate_average(student):
    return (
        float(student["Spanish"]) +
        float(student["English"]) +
        float(student["Social Studies"]) +
        float(student["Science"])
    ) / 4


def show_overall_average():
    students = load_students_from_csv()

    if not students:
        print("No students found.")
        return

    total = 0
    for student in students:
        total += calculate_average(student)

    overall = total / len(students)

    print("\n===== OVERALL AVERAGE =====")
    print(f"Students evaluated: {len(students)}")
    print(f"General average: {overall:.2f}")
