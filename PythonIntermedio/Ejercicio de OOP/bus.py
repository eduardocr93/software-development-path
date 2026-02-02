class Person:
    def __init__(self, name):
        self.name = name

class Bus:  
    def __init__(self, max_passengers):
        self.max_passengers = max_passengers
        self.passengers = []

    def add_passenger(self,person):
        if len (self.passengers) < self.max_passengers:
            self.passengers.append(person)
            print(f"{person.name} subió al bus.")
        else:
            print("El bus está lleno.")

    def remove_passenger(self):
        if self.passengers:
            person = self.passengers.pop()
            print(f"{person.name} bajó del bus")
        else:
            print("No hay pasajeros en el bus.")

        
p1 = Person("Ana")
p2 = Person("Luis")
p3 = Person("Carlos")

bus = Bus(2)
bus.add_passenger(p1)
bus.add_passenger(p2)
bus.add_passenger(p3)
bus.remove_passenger()
bus.remove_passenger()
bus.remove_passenger()