from actions.get_option import get_option


def get_classes(students):
    return sorted(set(student.student_class for student in students))


def choose_class(classes):
    print("\nSelect a class:")
    for i, cls in enumerate(classes, start=1):
        print(f"{i}. {cls}")
    print(f"{len(classes) + 1}. All students")

    return get_option(1, len(classes) + 1)


def filter_students_by_class(students, classes, class_choice):
    if class_choice == len(classes) + 1:
        return students, "All"

    selected_class = classes[class_choice - 1]
    return [s for s in students if s.student_class == selected_class], selected_class


def choose_student(filtered_students, selected_class):
    if not filtered_students:
        print("No students in that class.")
        return None

    print(f"\nStudents in {selected_class}:")
    for i, student in enumerate(filtered_students, start=1):
        print(f"{i}. {student.name} ({student.student_class})")

    student_choice = get_option(1, len(filtered_students))
    return filtered_students[student_choice - 1]


def confirm_deletion(student):
    print("\nSelected student:")
    print(f"Name: {student.name}")
    print(f"Class: {student.student_class}")

    confirm = input("Are you sure you want to delete this student? (y/n): ").strip().lower()
    return confirm == "y"


def delete_students(students):
    if not students:
        print("No students in memory.")
        return

    classes = get_classes(students)
    class_choice = choose_class(classes)

    filtered_students, selected_class = filter_students_by_class(
        students, classes, class_choice
    )

    selected_student = choose_student(filtered_students, selected_class)
    if not selected_student:
        return

    if not confirm_deletion(selected_student):
        print("Deletion cancelled.")
        return

    students.remove(selected_student)
    print("Student deleted successfully.")
