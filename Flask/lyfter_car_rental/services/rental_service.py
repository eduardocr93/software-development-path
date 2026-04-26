from lyfter_car_rental.db import get_connection

def create_rental(data):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO lyfter_car_rental.rentals (user_id, car_id, status)
                VALUES (%s, %s, %s) RETURNING id
            """, (data['user_id'], data['car_id'], 'ongoing'))
            rental_id = cur.fetchone()[0]

            cur.execute("UPDATE lyfter_car_rental.cars SET status='rented' WHERE id=%s", (data['car_id'],))
            conn.commit()
            return rental_id

def list_rentals(filters):
    query = "SELECT * FROM lyfter_car_rental.rentals WHERE TRUE"
    params = []
    for key, value in filters.items():
        query += f" AND {key}=%s"
        params.append(value)

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, params)
            columns = [desc[0] for desc in cur.description]
            rows = cur.fetchall()
            return [dict(zip(columns, row)) for row in rows]

def complete_rental(rental_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE lyfter_car_rental.rentals SET status='completed' WHERE id=%s RETURNING car_id",
                (rental_id,)
            )
            result = cur.fetchone()
            if not result:
                return {"error": "Alquiler no encontrado"}

            car_id = result[0]
            cur.execute("UPDATE lyfter_car_rental.cars SET status='available' WHERE id=%s", (car_id,))
            conn.commit()
            return {"message": "Alquiler completado"}

def update_rental_status(rental_id, status):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE lyfter_car_rental.rentals SET status=%s WHERE id=%s RETURNING id",
                (status, rental_id)
            )
            result = cur.fetchone()
            if not result:
                conn.rollback()
                return {"error": "Rental not found"}
            conn.commit()
            return {"message": "status updated"}
