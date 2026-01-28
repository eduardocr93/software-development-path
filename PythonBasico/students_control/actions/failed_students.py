from data.read_students import load_students_from_csv


def show_failed_students():
    students = load_students_from_csv()

    if not students:
        print("No students found.")
        return

    print("\n===== FAILED STUDENTS =====")
    found = False

    for student in students:
        failed_subjects = []

        if float(student["Spanish"]) < 60:
            failed_subjects.append(f"Spanish ({student['Spanish']})")
        if float(student["English"]) < 60:
            failed_subjects.append(f"English ({student['English']})")
        if float(student["Social Studies"]) < 60:
            failed_subjects.append(f"Social Studies ({student['Social Studies']})")
        if float(student["Science"]) < 60:
            failed_subjects.append(f"Science ({student['Science']})")

        if failed_subjects:
            found = True
            print(f"\nName: {student['Name']}")
            print(f"Class: {student['Class']}")
            print("Failed subjects:")
            for subject in failed_subjects:
                print(f" - {subject}")

    if not found:
        print("No failed students!")
