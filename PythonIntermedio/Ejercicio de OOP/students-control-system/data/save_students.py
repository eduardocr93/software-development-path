import csv
import os

def save_students_to_csv(students, filename="students.csv"):
    fieldnames = ['Name', 'Class', 'Spanish', 'English', 'Social Studies', 'Science']

    file_exists = os.path.exists(filename)

    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        for student in students:
            writer.writerow({
                'Name': student.name,
                'Class': student.student_class,
                'Spanish': student.spanish,
                'English': student.english,
                'Social Studies': student.social_studies,
                'Science': student.science
            })
