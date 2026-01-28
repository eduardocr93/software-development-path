import csv

def overwrite_students_to_csv(students, filename):
    import csv

    fieldnames = ['Name', 'Class', 'Spanish', 'English', 'Social Studies', 'Science']

    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for student in students:
            writer.writerow(student)
