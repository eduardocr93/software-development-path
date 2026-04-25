from faker import Faker
import random
from lyfter_car_rental.db import get_connection

fake = Faker()

def populate():
    conn = get_connection()
    cur = conn.cursor()

    try:

        cur.execute("TRUNCATE lyfter_car_rental.rentals RESTART IDENTITY CASCADE")
        cur.execute("TRUNCATE lyfter_car_rental.cars RESTART IDENTITY CASCADE")
        cur.execute("TRUNCATE lyfter_car_rental.users RESTART IDENTITY CASCADE")
        fake.unique.clear()

        users_data = []
        for _ in range(50):
            users_data.append((
                fake.name(),
                fake.unique.email(),
                fake.unique.user_name(),
                "1234",
                fake.date_of_birth(),
                "active"
            ))

        cur.executemany("""
            INSERT INTO lyfter_car_rental.users 
            (name, email, username, password, birth_date, status)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, users_data)

        brands = ["Toyota", "Honda", "Ford", "BMW", "Chevrolet"]
        models = ["Corolla", "Civic", "Focus", "X5", "Cruze"]

        cars_data = []
        for _ in range(50):
            cars_data.append((
                random.choice(brands),
                random.choice(models),
                random.randint(2000, 2023),
                "available"
            ))

        cur.executemany("""
            INSERT INTO lyfter_car_rental.cars 
            (brand, model, year, status)
            VALUES (%s, %s, %s, %s)
        """, cars_data)

        cur.execute("SELECT id FROM lyfter_car_rental.users")
        user_ids = [row[0] for row in cur.fetchall()]

        cur.execute("SELECT id FROM lyfter_car_rental.cars")
        car_ids = [row[0] for row in cur.fetchall()]

        rentals_data = []
        for _ in range(50):
            rentals_data.append((
                random.choice(user_ids),
                random.choice(car_ids),
                "ongoing"
            ))

        cur.executemany("""
            INSERT INTO lyfter_car_rental.rentals 
            (user_id, car_id, status)
            VALUES (%s, %s, %s)
        """, rentals_data)

        conn.commit()
        print("Datos insertados correctamente")

    except Exception as e:
        conn.rollback()
        print("Error:", e)

    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    populate()