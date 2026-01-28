import os
from data.read_students import load_students_from_csv
from data.overwrite_students import overwrite_students_to_csv


def import_students():
    filename = input("Enter file name to import (example: backup.csv): ").strip()

    if not filename.endswith(".csv"):
        filename += ".csv"

    if not os.path.exists(filename):
        print("That file does not exist.")
        return

    students = load_students_from_csv(filename)

    if not students:
        print("The file is empty or invalid.")
        return

    overwrite_students_to_csv(students, "students.csv")
    print("Data imported successfully!")
