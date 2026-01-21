def show_menu(actual):
    print(f"Número actual {actual}")
    print("1. Suma")
    print("2. Resta")
    print("3. Multiplicación")
    print("4. División")
    print("5. Borrar resultado")
    print("6. Salir")

def get_option():
    try:
        return int(input("Seleccione una opción: "))
    except ValueError:
        print("Ingrese un número válido por favor")
        return None

def get_number():
    try:
        return float(input("Digite el número: "))
    except ValueError:
        print("Número inválido")
        return None

def sumar(current, number):
    return current + number

def restar(current, number):
    return current - number

def multiplicar(current, number):
    return current * number

def dividir(current, number):
    try:
        if number == 0:
            raise ZeroDivisionError("No se puede dividir entre cero.")
        return current / number
    except ZeroDivisionError as e:
        print("Error:", e)
        return current

def calculator():
    current = 0
    while True:
        show_menu(current)
        option = get_option()

        if option is None:
            continue
        if option == 6:
            break
        if option not in [1, 2, 3, 4, 5]:
            print("Elija una opción válida")
            continue
        if option == 5:
            current = 0
            continue

        number = get_number()
        if number is None:
            continue

        if option == 1:
            current = sumar(current, number)
        elif option == 2:
            current = restar(current, number)
        elif option == 3:
            current = multiplicar(current, number)
        elif option == 4:
            current = dividir(current, number)

        print(f"El número actual es: {current}")

if __name__ == "__main__":
    calculator()
