from db import get_connection

def create_rental(data):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO lyfter_car_rental.rentals (user_id, car_id, status)
        VALUES (%s, %s, %s) RETURNING id
    """, (data['user_id'], data['car_id'], 'ongoing'))
    rental_id = cur.fetchone()[0]

    cur.execute("UPDATE lyfter_car_rental.cars SET status='rented' WHERE id=%s", (data['car_id'],))
    conn.commit()
    cur.close()
    conn.close()
    return rental_id

def list_rentals(filters):
    query = "SELECT * FROM lyfter_car_rental.rentals WHERE TRUE"
    params = []
    for key, value in filters.items():
        query += f" AND {key}=%s"
        params.append(value)

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(query, params)
    columns = [desc[0] for desc in cur.description]
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [dict(zip(columns, row)) for row in rows]

def complete_rental(rental_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("UPDATE lyfter_car_rental.rentals SET status='completed' WHERE id=%s", (rental_id,))

    cur.execute("SELECT car_id FROM lyfter_car_rental.rentals WHERE id=%s", (rental_id,))
    car_id = cur.fetchone()[0]

    cur.execute("UPDATE lyfter_car_rental.cars SET status='available' WHERE id=%s", (car_id,))
    conn.commit()
    cur.close()
    conn.close()
