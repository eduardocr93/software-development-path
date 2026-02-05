class HasWheels:
    def wheels(self):
        return "Tiene ruedas"

class HasEngine:
    def engine(self):
        return "Tiene motor"
    
class Bicycle(HasWheels):
    pass

class Car(HasWheels, HasEngine):
    pass

class Motorcycle(HasWheels, HasEngine):
    pass


bici = Bicycle()
carro = Car()
moto = Motorcycle()

print("Bici:", bici.wheels())
print("Carro:", carro.wheels(), "-", carro.engine())
print("Moto:", moto.wheels(), "-", moto.engine())