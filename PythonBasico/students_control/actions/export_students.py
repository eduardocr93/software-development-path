from data.read_students import load_students_from_csv
from data.overwrite_students import overwrite_students_to_csv


def export_students():
    students = load_students_from_csv()

    if not students:
        print("No students to export.")
        return

    filename = input("Enter export file name (example: backup.csv): ").strip()

    if not filename.endswith(".csv"):
        filename += ".csv"

    overwrite_students_to_csv(students, filename)
    print(f"Data exported successfully to {filename}")
