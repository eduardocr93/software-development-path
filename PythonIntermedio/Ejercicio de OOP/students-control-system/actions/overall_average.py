def calculate_average(student):
    return (
        student.spanish +
        student.english +
        student.social_studies +
        student.science
    ) / 4


def show_overall_average(students):

    if not students:
        print("No students in memory. Add or import first.")
        return

    total = 0
    for student in students:
        total += calculate_average(student)

    overall = total / len(students)

    print("\n===== OVERALL AVERAGE =====")
    print(f"Students evaluated: {len(students)}")
    print(f"General average: {overall:.2f}")
