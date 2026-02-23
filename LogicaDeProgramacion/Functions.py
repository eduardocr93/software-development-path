#1 
def print_name():
    variable_name= "Eduardo"
    return variable_name

def print_age():
    age=33
    print(f"{print_name()} tiene: {age} de edad")

print_age()

#------------------------------------
#2.1
#def function_local():
#    message = "Hello Inside"
#    print(message)

#function_local()

#print(message)

#------------------------------------
#2.2
counter = 0

def increment():
    global counter
    counter+=1
    print(f"Contador dentro de la función: {counter}")

increment()
increment()

#------------------------------------
#3
list_numbers = [4,6,2,29]

def sum_list (numbers):
    total = 0
    for num in numbers:
        total += num
    return total

print(sum_list(list_numbers))

#------------------------------------
#4
def reverse(text):
    return text[::-1]

print(reverse("Hello World"))

#------------------------------------
#5
def quantity_upper_lower(text):
    upper_count = 0
    lower_count = 0
    for char in text:
        if char.isupper():
            upper_count += 1
        elif char.islower():
            lower_count += 1
    return [upper_count, lower_count]


quantity = quantity_upper_lower("I love Nación Sushi")

print(f"El texto contiene {quantity[0]} letras en mayúsculas y {quantity[1]} letras en minúscula")

#------------------------------------
#6
def order_alphabetic(text):
    list_words = text.split("-")
    sorted_words = sorted(list_words)
    return "-".join(sorted_words)

print (order_alphabetic("python-variable-funcion-computadora-monitor"))

#------------------------------------
#7
def prime_number(numbers):
    primes = []
    for num in numbers:
        if num <= 1:
            continue
        is_prime = True
        for i in range(2, int(num**0.5) + 1):
            if num % i == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(num)
    return primes

print(f"El resultado de los números primos es {prime_number([1, 4, 6, 7, 13, 9, 67])}")