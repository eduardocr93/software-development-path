from contextlib import contextmanager
from sqlalchemy.exc import IntegrityError
from ORMs.db import SessionLocal
from ORMs.models import User, Car, Address

@contextmanager
def get_session():
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except IntegrityError as e:
        session.rollback()
        print("Error de integridad:", e)
    except Exception as e:
        session.rollback()
        print("Error inesperado:", e)
        raise
    finally:
        session.close()


class UserService:
    def create_user(self, name, email, username, password):
        with get_session() as session:
            if session.query(User).filter_by(username=username).first():
                print(f"Usuario con username '{username}' ya existe.")
                return
            if session.query(User).filter_by(email=email).first():
                print(f"Usuario con email '{email}' ya existe.")
                return
            user = User(name=name, email=email, username=username, password=password)
            session.add(user)

    def update_user(self, user_id, **kwargs):
        allowed_fields = {"name", "email", "username", "password"}
        with get_session() as session:
            user = session.get(User, user_id)
            if not user:
                print("Usuario no encontrado")
                return
            for key, value in kwargs.items():
                if key in allowed_fields:
                    setattr(user, key, value)

    def delete_user(self, user_id):
        with get_session() as session:
            user = session.get(User, user_id)
            if user:
                session.delete(user)

    def list_users(self):
        with get_session() as session:
            users = session.query(User).all()
            return [{"id": u.id, "name": u.name, "email": u.email} for u in users]


class CarService:
    def create_car(self, brand, model, year):
        with get_session() as session:
            car = Car(brand=brand, model=model, year=year)
            session.add(car)

    def update_car(self, car_id, **kwargs):
        allowed_fields = {"brand", "model", "year", "user_id"}
        with get_session() as session:
            car = session.get(Car, car_id)
            if not car:
                print("Auto no encontrado")
                return
            for key, value in kwargs.items():
                if key in allowed_fields:
                    setattr(car, key, value)

    def delete_car(self, car_id):
        with get_session() as session:
            car = session.get(Car, car_id)
            if car:
                session.delete(car)

    def assign_car_to_user(self, car_id, user_id):
        with get_session() as session:
            car = session.get(Car, car_id)
            if car:
                car.user_id = user_id

    def list_cars(self):
        with get_session() as session:
            cars = session.query(Car).all()
            return [
                {"id": c.id, "brand": c.brand, "model": c.model, "year": c.year, "user_id": c.user_id}
                for c in cars
            ]


class AddressService:
    def create_address(self, street, city, user_id):
        with get_session() as session:
            address = Address(street=street, city=city, user_id=user_id)
            session.add(address)

    def update_address(self, address_id, **kwargs):
        allowed_fields = {"street", "city", "user_id"}
        with get_session() as session:
            address = session.get(Address, address_id)
            if not address:
                print("Dirección no encontrada")
                return
            for key, value in kwargs.items():
                if key in allowed_fields:
                    setattr(address, key, value)

    def delete_address(self, address_id):
        with get_session() as session:
            address = session.get(Address, address_id)
            if address:
                session.delete(address)

    def list_addresses(self):
        with get_session() as session:
            addresses = session.query(Address).all()
            return [
                {"id": a.id, "street": a.street, "city": a.city, "user_id": a.user_id}
                for a in addresses
            ]
