import os
from data.read_students import load_students_from_csv


def import_students(students):
    filename = input("Enter file name to import (example: backup.csv): ").strip()

    if not filename.endswith(".csv"):
        filename += ".csv"

    if not os.path.exists(filename):
        print("That file does not exist.")
        return

    loaded_students = load_students_from_csv(filename)

    if not loaded_students:
        print("The file is empty or invalid.")
        return

    students.clear()
    students.extend(loaded_students)
    print("Data imported into memory successfully")