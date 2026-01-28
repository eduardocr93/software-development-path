def load_students_from_csv(filename="students.csv"):
    import csv
    import os

    if not os.path.exists(filename):
        return []

    students = []
    with open(filename, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            students.append(row)

    return students