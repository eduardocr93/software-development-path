import csv
import os
from models.student import Student


def load_students_from_csv(filename="students.csv"):

    if not os.path.exists(filename):
        return []

    students = []
    with open(filename, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            students.append(
                Student(
                    name=row["Name"],
                    student_class=row["Class"],
                    spanish=float(row["Spanish"]),
                    english=float(row["English"]),
                    social_studies=float(row["Social Studies"]),
                    science=float(row["Science"])
                )
            )

    return students
