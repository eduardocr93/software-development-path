import random
secret_number = random.randint(1, 10)

print (secret_number)

print("Adivina el número secreto (entre 1 y 10)")

while True:
    intento = int(input("Ingresa tu número: "))
    
    if intento == secret_number:
        print("¡Correcto! El número secreto era", secret_number)
        break
    else:
        print("Incorrecto, intenta de nuevo")
