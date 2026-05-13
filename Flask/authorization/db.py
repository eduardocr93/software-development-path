from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    Integer,
    String,
    Float,
    DateTime,
    ForeignKey,
    insert,
    select,
    update,
    delete
)

from datetime import datetime

metadata_obj = MetaData()

user_table = Table(
    "users",
    metadata_obj,

    Column("id", Integer, primary_key=True),
    Column("username", String(30)),
    Column("password", String),
    Column("role", String(20))
)

product_table = Table(
    "products",
    metadata_obj,

    Column("id", Integer, primary_key=True),
    Column("nombre", String(50)),
    Column("precio", Float),
    Column("fecha_entrada", DateTime),
    Column("cantidad", Integer)
)

invoice_table = Table(
    "invoices",
    metadata_obj,

    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("product_id", Integer, ForeignKey("products.id")),
    Column("cantidad", Integer),
    Column("total", Float),
    Column("fecha", DateTime)
)


class DB_Manager:

    def __init__(self):

        self.engine = create_engine(
            "postgresql+psycopg2://postgres:postgres@localhost:5432/postgres"
        )

        metadata_obj.create_all(self.engine)

    def insert_user(self, username, password, role):

        stmt = insert(user_table).returning(
            user_table.c.id
        ).values(
            username=username,
            password=password,
            role=role
        )

        with self.engine.connect() as conn:

            result = conn.execute(stmt)

            conn.commit()

        return result.all()[0]

    def get_user(self, username, password):

        stmt = select(user_table).where(
            user_table.c.username == username
        ).where(
            user_table.c.password == password
        )

        with self.engine.connect() as conn:

            result = conn.execute(stmt)

            users = result.all()

            if len(users) == 0:

                return None

            return users[0]

    def get_user_by_id(self, id):

        stmt = select(user_table).where(
            user_table.c.id == id
        )

        with self.engine.connect() as conn:

            result = conn.execute(stmt)

            users = result.all()

            if len(users) == 0:

                return None

            return users[0]

    def insert_product(self, nombre, precio, cantidad):

        stmt = insert(product_table).values(
            nombre=nombre,
            precio=precio,
            fecha_entrada=datetime.now(),
            cantidad=cantidad
        )

        with self.engine.connect() as conn:

            conn.execute(stmt)

            conn.commit()

    def get_products(self):

        stmt = select(product_table)

        with self.engine.connect() as conn:

            result = conn.execute(stmt)

            return result.all()

    def get_product_by_id(self, id):

        stmt = select(product_table).where(
            product_table.c.id == id
        )

        with self.engine.connect() as conn:

            result = conn.execute(stmt)

            products = result.all()

            if len(products) == 0:

                return None

            return products[0]

    def update_product(self, id, nombre, precio, cantidad):

        stmt = update(product_table).where(
            product_table.c.id == id
        ).values(
            nombre=nombre,
            precio=precio,
            cantidad=cantidad
        )

        with self.engine.connect() as conn:

            conn.execute(stmt)

            conn.commit()

    def delete_product(self, id):

        stmt = delete(product_table).where(
            product_table.c.id == id
        )

        with self.engine.connect() as conn:

            conn.execute(stmt)

            conn.commit()

    def create_invoice(self, user_id, product_id, cantidad, total):

        stmt = insert(invoice_table).values(
            user_id=user_id,
            product_id=product_id,
            cantidad=cantidad,
            total=total,
            fecha=datetime.now()
        )

        with self.engine.connect() as conn:

            conn.execute(stmt)

            conn.commit()

    def get_invoices_by_user(self, user_id):

        stmt = select(invoice_table).where(
            invoice_table.c.user_id == user_id
        )

        with self.engine.connect() as conn:

            result = conn.execute(stmt)

            return result.all()

    def reduce_stock(self, product_id, cantidad):

        product = self.get_product_by_id(product_id)

        if product is None:

            return False

        new_quantity = product[4] - cantidad

        if new_quantity < 0:

            return False

        stmt = update(product_table).where(
            product_table.c.id == product_id
        ).values(
            cantidad=new_quantity
        )

        with self.engine.connect() as conn:

            conn.execute(stmt)

            conn.commit()

        return True