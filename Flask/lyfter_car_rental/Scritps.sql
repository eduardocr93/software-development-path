CREATE SCHEMA IF NOT EXISTS lyfter_car_rental;

CREATE TABLE IF NOT EXISTS lyfter_car_rental.users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(200) NOT NULL,
    birth_date DATE NOT NULL,
    status VARCHAR(20) DEFAULT 'active'
);

CREATE TABLE IF NOT EXISTS lyfter_car_rental.cars (
    id SERIAL PRIMARY KEY,
    brand VARCHAR(50) NOT NULL,
    model VARCHAR(50) NOT NULL,
    year INT NOT NULL,
    status VARCHAR(20) DEFAULT 'available'
);

CREATE TABLE IF NOT EXISTS lyfter_car_rental.rentals (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES lyfter_car_rental.users(id),
    car_id INT REFERENCES lyfter_car_rental.cars(id),
    rental_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'ongoing'
);

INSERT INTO lyfter_car_rental.users (name, email, username, password, birth_date, status)
VALUES ('Juan Pérez', 'juan@example.com', 'juanp', '1234', '1990-05-10', 'active');

INSERT INTO lyfter_car_rental.cars (brand, model, year, status)
VALUES ('Toyota', 'Corolla', 2020, 'available');

UPDATE lyfter_car_rental.users SET status='inactive' WHERE id=1;

UPDATE lyfter_car_rental.cars SET status='maintenance' WHERE id=2;

INSERT INTO lyfter_car_rental.rentals (user_id, car_id, status)
VALUES (1, 1, 'ongoing');
UPDATE lyfter_car_rental.cars SET status='rented' WHERE id=1;

UPDATE lyfter_car_rental.rentals SET status='completed' WHERE id=1;
UPDATE lyfter_car_rental.cars SET status='available' WHERE id=2;

UPDATE lyfter_car_rental.cars SET status='disabled' WHERE id=3;

SELECT * FROM lyfter_car_rental.cars WHERE status='rented';

SELECT * FROM lyfter_car_rental.cars WHERE status='available';
