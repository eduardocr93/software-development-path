from flask import Flask
from routes.user_routes import user_bp
from routes.car_routes import car_bp
from routes.rental_routes import rental_bp

app = Flask(__name__)

app.register_blueprint(user_bp)
app.register_blueprint(car_bp)
app.register_blueprint(rental_bp)

if __name__ == "__main__":
    app.run(debug=True)
