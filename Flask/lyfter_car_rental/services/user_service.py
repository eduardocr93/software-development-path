from db import get_connection

def create_user(data):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO lyfter_car_rental.users (name, email, username, password, birth_date, status)
                VALUES (%s, %s, %s, %s, %s, %s) RETURNING id
            """, (data['name'], data['email'], data['username'], data['password'], data['birth_date'], 'active'))
            user_id = cur.fetchone()[0]
            conn.commit()
            return user_id


def list_users(filters):
    query = "SELECT * FROM lyfter_car_rental.users WHERE TRUE"
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

def update_user_status(user_id, status):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE lyfter_car_rental.users SET status=%s WHERE id=%s", (status, user_id))
    conn.commit()
    cur.close()
    conn.close()

