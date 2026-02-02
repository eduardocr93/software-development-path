def calculate_average(student):
    return (
        student.spanish +
        student.english +
        student.social_studies +
        student.science
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
        print(f"Name: {student.name}")
        print(f"Class: {student.student_class}")
        print(f"Average: {avg:.2f}")
