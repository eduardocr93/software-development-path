from config.database import db


class Invoice(db.Model):

    __tablename__ = "invoices"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    invoice_number = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    billing_address = db.Column(
        db.String(255),
        nullable=False
    )

    payment_method = db.Column(
        db.String(50),
        nullable=False
    )

    total = db.Column(
        db.Float,
        nullable=False
    )

    status = db.Column(
        db.String(20),
        default="PAID"
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    user = db.relationship(
        "User",
        backref="invoices"
    )