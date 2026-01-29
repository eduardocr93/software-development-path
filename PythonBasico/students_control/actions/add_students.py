from actions.get_option import get_option


def get_valid_grade(subject):
    while True:
        try:
            grade = float(input(f"{subject}: "))
            if 0 <= grade <= 100:
                return grade
            else:
                print("Grade must be between 0 and 100.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def get_valid_class():
    while True:
        class_input = input("Class: ").upper()

        if len(class_input) < 2:
            print("Invalid class format. Example: 10A, 9B")
            continue

        number_part = class_input[:-1]
        letter_part = class_input[-1]

        if not number_part.isdigit():
            print("Class must start with a number.")
            continue

        if not letter_part.isalpha() or len(letter_part) != 1:
            print("Class must end with a letter (A-Z).")
            continue

        return class_input


def get_valid_name():
    while True:
        name = input("Full name: ").strip()
        if name:
            return name
        print("Name cannot be empty.")


def get_student_data():
    name = get_valid_name()
    student_class = get_valid_class()
    spanish = get_valid_grade("Spanish")
    english = get_valid_grade("English")
    social_studies = get_valid_grade("Social Studies")
    science = get_valid_grade("Science")

    return {
        'Name': name,
        'Class': student_class,
        'Spanish': spanish,
        'English': english,
        'Social Studies': social_studies,
        'Science': science
    }


def add_student(students):
    student = get_student_data()
    students.append(student)


def add_students_loop(students):
    while True:
        add_student(students)

        print("Do you want to add another student?")
        print("1. Yes")
        print("2. Return")

        choice = get_option(1, 2)
        if choice == 2:
            break


def validate_students_data(students):
    add_students_loop(students)
