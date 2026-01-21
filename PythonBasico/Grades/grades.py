passed_count = 0
failed_count = 0
passed_sum = 0
failed_sum = 0
total_sum = 0

total_grades = int(input("Ingrese el número de notas: "))

for i in range(total_grades):
    grade = float(input(f"Ingrese la nota {i+1}: "))
    total_sum += grade

    if grade >= 70:
        passed_count += 1
        passed_sum += grade
    else:
        failed_count += 1
        failed_sum += grade

average_total = total_sum / total_grades 

if passed_count > 0:
    average_passed = passed_sum / passed_count
else:
    average_passed = "No hay notas aprobadas"

if failed_count > 0:
    average_failed = failed_sum / failed_count
else:
    average_failed = "No hay notas reprobadas"


print("Número de notas pasadas:", passed_count)
print("Número de notas perdidas:", failed_count)
print("Promedio de todas las notas:", average_total)
print("Promedio de notas pasadas:", average_passed)
print("Promedio de tareas falladas:", average_failed)
