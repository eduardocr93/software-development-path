name = input ("Ingrese su nombre: ")
lastName = input ("Ingrese su apellido: ")
age = int(input ("Ingrese su edad en números: "))

if age < 3:
    stage = "bebé"
elif age < 12:
    stage = "niño"
elif age < 15:
    stage = "preadolescente"
elif age < 18:
    stage = "adolescente"
elif age < 30:
    stage = "adulto joven"
elif age < 62:
    stage = "adulto"
else:
    stage = "adulto mayor"

print(f"{name} {lastName}, con {age} años, es {stage}")
