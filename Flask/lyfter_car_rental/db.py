import psycopg2
from lyfter_car_rental.config import DB_CONFIG

def get_connection():
    return psycopg2.connect(**DB_CONFIG)
