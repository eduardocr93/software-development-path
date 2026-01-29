from actions.get_option import get_option
from actions.add_students import validate_students_data
from actions.show_students import show_students
from actions.top_students import show_top_3_students
from actions.overall_average import show_overall_average
from actions.export_students import export_students
from actions.import_students import import_students
from actions.delete_students import delete_students
from actions.failed_students import show_failed_students

def show_menu():
    print("1. Add student")
    print("2. Student information")
    print("3. Top 3")
    print("4. Overall average of students")
    print("5. Export data")
    print("6. Import data")
    print("7. Delete students")
    print("8. Failed students")
    print("9. Exit")

def validate_menu_options(students):
    while True:
        show_menu()
        option = get_option(1, 9)

        if option == 9:
            break

        if option == 1:
            validate_students_data(students)
        elif option == 2:
            show_students(students)
        elif option == 3:
            show_top_3_students(students)
        elif option == 4:
            show_overall_average(students)
        elif option == 5:
            export_students(students)
        elif option == 6:
            import_students(students)
        elif option == 7:
            delete_students(students)
        elif option == 8:
            show_failed_students(students)
