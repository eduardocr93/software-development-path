from db import get_connection

def create_car(data):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO lyfter_car_rental.cars (brand, model, year, status)
        VALUES (%s, %s, %s, %s) RETURNING id
    """, (data['brand'], data['model'], data['year'], 'available'))
    car_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return car_id

def list_cars(filters):
    query = "SELECT * FROM lyfter_car_rental.cars WHERE TRUE"
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

def update_car_status(car_id, status):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE lyfter_car_rental.cars SET status=%s WHERE id=%s", (status, car_id))
    conn.commit()
    cur.close()
    conn.close()
