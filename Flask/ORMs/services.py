from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from ORMs.models import User, Car, Address, Base
from contextlib import contextmanager

engine = create_engine("sqlite:///car_rental.db")
Session = sessionmaker(bind=engine)

@contextmanager
def get_session():
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


class UserService:
    def create_user(self, name, email, username, password):
        with get_session() as session:
            existing = session.query(User).filter_by(username=username).first()
            if existing:
                print(f"Usuario con username '{username}' ya existe.")
                return
            user = User(name=name, email=email, username=username, password=password)
            session.add(user)

    def update_user(self, user_id, **kwargs):
        with get_session() as session:
            user = session.get(User, user_id)
            if not user:
                raise ValueError("Usuario no encontrado")
            for key, value in kwargs.items():
                setattr(user, key, value)

    def delete_user(self, user_id):
        with get_session() as session:
            user = session.get(User, user_id)
            if not user:
                raise ValueError("Usuario no encontrado")
            session.delete(user)

    def list_users(self):
        with get_session() as session:
            users = session.query(User).all()
            return [
                {"id": u.id, "name": u.name, "email": u.email, "username": u.username}
                for u in users
            ]



class CarService:
    def create_car(self, brand, model, year, user_id=None):
        with get_session() as session:
            car = Car(brand=brand, model=model, year=year, user_id=user_id)
            session.add(car)

    def update_car(self, car_id, **kwargs):
        with get_session() as session:
            car = session.get(Car, car_id)
            if not car:
                raise ValueError("Automóvil no encontrado")
            for key, value in kwargs.items():
                setattr(car, key, value)

    def delete_car(self, car_id):
        with get_session() as session:
            car = session.get(Car, car_id)
            if not car:
                raise ValueError("Automóvil no encontrado")
            session.delete(car)

    def list_cars(self):
        with get_session() as session:
            cars = session.query(Car).all()
            return [
                {
                    "id": c.id,
                    "brand": c.brand,
                    "model": c.model,
                    "year": c.year,
                    "user_id": c.user_id
                }
                for c in cars
            ]


    def assign_car_to_user(self, car_id, user_id):
        with get_session() as session:
            car = session.get(Car, car_id)
            if not car:
                raise ValueError("Automóvil no encontrado")
            user = session.get(User, user_id)
            if not user:
                raise ValueError("Usuario no encontrado")
            car.user_id = user.id


class AddressService:
    def create_address(self, street, city, user_id):
        with get_session() as session:
            user = session.get(User, user_id)
            if not user:
                raise ValueError("Usuario no encontrado")
            address = Address(street=street, city=city, user_id=user_id)
            session.add(address)

    def update_address(self, address_id, **kwargs):
        with get_session() as session:
            address = session.get(Address, address_id)
            if not address:
                raise ValueError("Dirección no encontrada")
            for key, value in kwargs.items():
                setattr(address, key, value)

    def delete_address(self, address_id):
        with get_session() as session:
            address = session.get(Address, address_id)
            if not address:
                raise ValueError("Dirección no encontrada")
            session.delete(address)

    def list_addresses(self):
        with get_session() as session:
            addresses = session.query(Address).all()
            return [
                {
                    "id": a.id,
                    "street": a.street,
                    "city": a.city,
                    "user_id": a.user_id
                }
                for a in addresses
            ]
