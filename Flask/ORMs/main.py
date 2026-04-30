from ORMs.services import UserService, CarService, AddressService

def main():
    u_service = UserService()
    c_service = CarService()
    a_service = AddressService()

    # Crear usuarios
    print("=== Crear Usuarios ===")
    u_service.create_user("Eduardo", "edu@example.com", "eduardo", "1234")
    u_service.create_user("Eduardo", "edu1@example.com", "eduardo1", "1234")
    u_service.create_user("Maria", "maria@example.com", "maria", "abcd")

    # Crear direcciones asociadas a cada usuario
    print("=== Crear Direcciones ===")
    a_service.create_address("Calle 123", "San José", 1)
    a_service.create_address("Avenida Central", "San José", 2)
    a_service.create_address("Boulevard Morazán", "Heredia", 3)

    # Crear autos asociados a cada usuario
    print("=== Crear Autos ===")
    c_service.create_car("Toyota", "Corolla", 2020)
    c_service.assign_car_to_user(1, 1)

    c_service.create_car("Honda", "Civic", 2019)
    c_service.assign_car_to_user(2, 2)

    c_service.create_car("Nissan", "Sentra", 2021)
    c_service.assign_car_to_user(3, 3)

    # Listar usuarios
    print("=== Usuarios ===")
    for user in u_service.list_users():
        print(f"ID: {user['id']}, Nombre: {user['name']}, Email: {user['email']}")

    # Listar direcciones
    print("=== Direcciones ===")
    for address in a_service.list_addresses():
        print(f"ID: {address['id']}, Calle: {address['street']}, Ciudad: {address['city']}, UsuarioID: {address['user_id']}")

    # Listar autos
    print("=== Autos ===")
    for car in c_service.list_cars():
        print(f"ID: {car['id']}, Marca: {car['brand']}, Modelo: {car['model']}, Año: {car['year']}, UsuarioID: {car['user_id']}")

if __name__ == "__main__":
    main()
