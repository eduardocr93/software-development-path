from data.read_students import load_students_from_csv
from data.overwrite_students import overwrite_students_to_csv
from actions.get_option import get_option


def delete_students():
    students = load_students_from_csv()

    if not students:
        print("No students found.")
        return

    classes = sorted(set(student["Class"] for student in students))

    print("\nSelect a class:")
    for i, cls in enumerate(classes, start=1):
        print(f"{i}. {cls}")
    print(f"{len(classes) + 1}. All students")

    class_choice = get_option(1, len(classes) + 1)

    if class_choice == len(classes) + 1:
        filtered_students = students
        selected_class = "All"
    else:
        selected_class = classes[class_choice - 1]
        filtered_students = [s for s in students if s["Class"] == selected_class]

    print(f"\nStudents in {selected_class}:")
    for i, student in enumerate(filtered_students, start=1):
        print(f"{i}. {student['Name']} ({student['Class']})")

    student_choice = get_option(1, len(filtered_students))
    selected_student = filtered_students[student_choice - 1]

    print("\nSelected student:")
    print(f"Name: {selected_student['Name']}")
    print(f"Class: {selected_student['Class']}")

    confirm = input("Are you sure you want to delete this student? (y/n): ").lower()
    if confirm != "y":
        print("Deletion cancelled.")
        return

    updated_students = [s for s in students if s != selected_student]
    overwrite_students_to_csv(updated_students, "students.csv")

    print("Student deleted successfully.")
