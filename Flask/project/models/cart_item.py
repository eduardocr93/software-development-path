from config.database import db


class CartItem(db.Model):

    __tablename__ = "cart_items"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    cart_id = db.Column(
        db.Integer,
        db.ForeignKey("carts.id"),
        nullable=False
    )

    product_id = db.Column(
        db.Integer,
        db.ForeignKey("products.id"),
        nullable=False
    )

    quantity = db.Column(
        db.Integer,
        nullable=False
    )

    cart = db.relationship(
        "Cart",
        backref="items"
    )

    product = db.relationship(
        "Product"
    )