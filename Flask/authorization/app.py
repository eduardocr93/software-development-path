from flask import Flask, request, jsonify, Response

from auth import token_required, admin_required
from db import DB_Manager
from jwt_manager import JWT_Manager

app = Flask("authorization-service")

db_manager = DB_Manager()

jwt_manager = JWT_Manager()


@app.route("/liveness")
def liveness():

    return "<p>Server running</p>"


@app.route('/register', methods=['POST'])
def register():

    try:

        data = request.get_json()

        if (
            data.get("username") is None or
            data.get("password") is None
        ):

            return Response(status=400)

        role = "user"

        result = db_manager.insert_user(
            data.get("username"),
            data.get("password"),
            role
        )

        user_id = result[0]

        token = jwt_manager.encode({
            "id": user_id,
            "role": role
        })

        return jsonify(token=token)

    except Exception as e:

        print(e)

        return Response(status=500)


@app.route('/login', methods=['POST'])
def login():

    try:

        data = request.get_json()

        if (
            data.get("username") is None or
            data.get("password") is None
        ):

            return Response(status=400)

        user = db_manager.get_user(
            data.get("username"),
            data.get("password")
        )

        if user is None:

            return Response(status=403)

        token = jwt_manager.encode({
            "id": user[0],
            "role": user[3]
        })

        return jsonify(token=token)

    except Exception as e:

        print(e)

        return Response(status=500)


@app.route('/me')
@token_required
def me():

    try:

        user_id = request.user["id"]

        user = db_manager.get_user_by_id(user_id)

        if user is None:

            return Response(status=404)

        return jsonify(
            id=user[0],
            username=user[1],
            role=user[3]
        )

    except Exception as e:

        print(e)

        return Response(status=500)


@app.route('/products', methods=['POST'])
@admin_required
def create_product():

    try:

        data = request.get_json()

        if (
            data.get("nombre") is None or
            data.get("precio") is None or
            data.get("cantidad") is None
        ):

            return Response(status=400)

        db_manager.insert_product(
            data.get("nombre"),
            data.get("precio"),
            data.get("cantidad")
        )

        return Response(status=201)

    except Exception as e:

        print(e)

        return Response(status=500)


@app.route('/products', methods=['GET'])
@token_required
def get_products():

    try:

        products = db_manager.get_products()

        result = []

        for product in products:

            result.append({
                "id": product[0],
                "nombre": product[1],
                "precio": product[2],
                "fecha_entrada": product[3],
                "cantidad": product[4]
            })

        return jsonify(result)

    except Exception as e:

        print(e)

        return Response(status=500)


@app.route('/products/<id>', methods=['PUT'])
@admin_required
def update_product(id):

    try:

        data = request.get_json()

        if (
            data.get("nombre") is None or
            data.get("precio") is None or
            data.get("cantidad") is None
        ):

            return Response(status=400)

        db_manager.update_product(
            id,
            data.get("nombre"),
            data.get("precio"),
            data.get("cantidad")
        )

        return Response(status=200)

    except Exception as e:

        print(e)

        return Response(status=500)


@app.route('/products/<id>', methods=['DELETE'])
@admin_required
def delete_product(id):

    try:

        db_manager.delete_product(id)

        return Response(status=200)

    except Exception as e:

        print(e)

        return Response(status=500)

@app.route('/buy', methods=['POST'])
@token_required
def buy_product():

    try:

        data = request.get_json()

        if (
            data.get("product_id") is None or
            data.get("cantidad") is None
        ):

            return Response(status=400)

        product = db_manager.get_product_by_id(
            data.get("product_id")
        )

        if product is None:

            return Response(status=404)

        cantidad = data.get("cantidad")

        if product[4] < cantidad:

            return jsonify(
                error="Not enough stock"
            ), 400

        total = product[2] * cantidad

        success = db_manager.reduce_stock(
            product[0],
            cantidad
        )

        if not success:

            return Response(status=400)

        db_manager.create_invoice(
            request.user["id"],
            product[0],
            cantidad,
            total
        )

        return jsonify(
            message="Purchase completed",
            total=total
        )

    except Exception as e:

        print(e)

        return Response(status=500)

@app.route('/invoices', methods=['GET'])
@token_required
def get_invoices():

    try:

        invoices = db_manager.get_invoices_by_user(
            request.user["id"]
        )

        result = []

        for invoice in invoices:

            result.append({
                "id": invoice[0],
                "product_id": invoice[2],
                "cantidad": invoice[3],
                "total": invoice[4]
            })

        return jsonify(result)

    except Exception as e:

        print(e)

        return Response(status=500)


if __name__ == "__main__":

    app.run(debug=True)