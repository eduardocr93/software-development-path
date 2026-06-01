from models.product import Product
from config.database import db
from config.cache import cache
from exceptions import BadRequestError, NotFoundError
from services.validation import (
    validate_json,
    validate_number,
    validate_integer,
    validate_optional_string,
    validate_required_string
)

class ProductService:

    @staticmethod
    def get_all_products():

        cached_data = cache.get("products_all")

        if cached_data:
            return cached_data, 200

        products = Product.query.all()

        response = [
            {
                "id": product.id,
                "name": product.name,
                "description": product.description,
                "price": product.price,
                "stock": product.stock,
                "category": product.category
            }
            for product in products
        ]

        cache.set("products_all",response,ttl=60)

        return response, 200

    @staticmethod
    def get_product_by_id(product_id):

        cache_key = (f"product_{product_id}")

        cached_data = cache.get(cache_key)

        if cached_data:
            return cached_data, 200

        product = db.session.get(
            Product,
            product_id
        )

        if not product:
            raise NotFoundError("Product not found")

        response = {
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "stock": product.stock,
            "category": product.category
        }

        cache.set(cache_key,response,ttl=60)

        return response, 200

    @staticmethod
    def create_product(data):

        validate_json(data)
        validate_required_string(data, "name")
        validate_number(data, "price", min_value=0)
        validate_integer(data, "stock", min_value=0)
        validate_optional_string(data, "description")
        validate_optional_string(data, "category")

        product = Product(
            name=data["name"],
            description=data.get("description"),
            price=data["price"],
            stock=data["stock"],
            category=data.get("category")
        )

        db.session.add(product)
        db.session.commit()

        cache.delete("products_all")

        return {"message": "Product created successfully"}, 201

    @staticmethod
    def update_product(product_id, data):

        validate_json(data)

        if not data:
            raise BadRequestError("No update data provided")

        product = db.session.get(
            Product,
            product_id
        )

        if not product:
            raise NotFoundError("Product not found")

        if "name" in data:
            validate_required_string(data, "name")
            product.name = data["name"]

        if "description" in data:
            validate_optional_string(data, "description")
            product.description = data["description"]

        if "price" in data:
            validate_number(data, "price", min_value=0)
            product.price = data["price"]

        if "stock" in data:
            validate_integer(data, "stock", min_value=0)
            product.stock = data["stock"]

        if "category" in data:
            validate_optional_string(data, "category")
            product.category = data["category"]

        db.session.commit()

        cache.delete("products_all")

        cache.delete(f"product_{product_id}")

        return {"message": "Product updated successfully"}, 200

    @staticmethod
    def delete_product(product_id):

        product = db.session.get(
            Product,
            product_id
        )

        if not product:
            raise NotFoundError("Product not found")

        db.session.delete(product)
        db.session.commit()

        cache.delete("products_all")

        cache.delete(f"product_{product_id}")

        return {"message": "Product deleted successfully"}, 200