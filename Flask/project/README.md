# Petshop Backend - Flask Project

API backend para un e-commerce de productos para mascotas. Proyecto desarrollado con Flask, SQLAlchemy, PostgreSQL, Redis y JWT.

## Contenido

- `app.py` — Inicialización de Flask, registro de blueprints y manejo global de errores.
- `config/` — Configuración de base de datos y variables de entorno.
- `decorators/` — Decoradores de autorización y roles.
- `models/` — Modelos SQLAlchemy.
- `routes/` — Rutas y blueprints por módulo.
- `services/` — Lógica de negocio y validaciones.
- `tests/` — Pruebas automáticas con `pytest`.
- `migrations/` — Configuración de Flask-Migrate.

## Requisitos

- Python 3.11+ (compatible con 3.14)
- PostgreSQL
- Redis (opcional, para cacheo de productos)

El caché es opcional: si Redis no está disponible, los endpoints de productos continúan consultando la base de datos y se registra una advertencia.

## Configuración

1. Abre la terminal en `Project`.
2. Copia el archivo de ejemplo y actualiza los valores:

```bash
copy .env.example .env
```

3. Ajusta `.env` con tu configuración local:

- `SQLALCHEMY_DATABASE_URI` — conexión a PostgreSQL.
- `JWT_SECRET_KEY` — clave secreta para JWT.
- `JWT_ACCESS_TOKEN_EXPIRES` — expiración del token.
- `REDIS_HOST`, `REDIS_PORT`, `REDIS_USERNAME`, `REDIS_PASSWORD`, `REDIS_DB` — datos de Redis.
- `FRONTEND_ORIGINS` — orígenes permitidos para el frontend, separados por comas. Por defecto permite `http://127.0.0.1:8765`, `http://localhost:8765`, `http://127.0.0.1:5500` y `http://localhost:5500`.

4. Instala las dependencias:

```bash
pip install -r requirements.txt
```

## Ejecución

Desde `Project`:

```bash
python app.py
```

Abre en el navegador o Postman:

```
http://127.0.0.1:5000
```

Para usar el frontend de `JavaScript/PetStore`, inicia su servidor local en el puerto `8765` (o configura el origen que uses en `FRONTEND_ORIGINS`). CORS solo se habilita para los orígenes enumerados y no acepta credenciales de cookies.

Para habilitar una cuenta de administración, primero regístrala como cliente y luego ejecuta desde esta carpeta:

```bash
python -m flask promote-admin correo@ejemplo.com
```

El comando solo está disponible en la CLI local; no existe un endpoint público para elevar roles. Cierra sesión e inicia sesión de nuevo para que el token incluya el nuevo rol.

## Migraciones

El proyecto incluye `Flask-Migrate`. Si necesitas actualizar el esquema:

```bash
python -m flask db migrate -m "Descripción"
python -m flask db upgrade
```


## Endpoints

### 1. Autenticación

- `POST /auth/register`
  - Registra usuario.
  - Body mínimo:
    ```json
    {
      "name": "Usuario",
      "email": "usuario@test.com",
      "password": "123456"
    }
    ```
- `POST /auth/login`
  - Obtiene token JWT.
  - Body:
    ```json
    {
      "email": "usuario@test.com",
      "password": "123456"
    }
    ```
- `GET /auth/admin-test`
  - Prueba de autorización admin.
  - Requiere token admin.

### 2. Productos

- `GET /products/` — Listar productos.
- `GET /products/<product_id>` — Ver producto.
- `POST /products/` — Crear producto (admin):
  ```json
  {
    "name": "Producto",
    "description": "Descripción",
    "price": 12000,
    "stock": 10
  }
  ```
- `PUT /products/<product_id>` — Actualizar producto (admin).
- `DELETE /products/<product_id>` — Eliminar producto (admin).

### 3. Carrito

- `POST /carts/` — Crea un carrito activo para el usuario.
- `GET /carts/my-cart` — Obtiene el carrito actual.
- `POST /carts/items` — Agrega producto al carrito:
  ```json
  {
    "product_id": 1,
    "quantity": 2
  }
  ```
- `PUT /carts/items/<item_id>` — Actualiza cantidad:
  ```json
  {
    "quantity": 3
  }
  ```
- `DELETE /carts/items/<item_id>` — Elimina item del carrito.

### 4. Facturas / Checkout

- `POST /invoices/checkout`
  - Finaliza compra.
  - Body:
    ```json
    {
      "billing_address": "Mi dirección",
      "payment_method": "SINPE"
    }
    ```
- `GET /invoices/` — Lista facturas del usuario.
- `GET /invoices/admin` — Lista todas las facturas para el panel de administración (admin).
- `GET /invoices/<invoice_id>` — Detalle de factura.
- `POST /invoices/<invoice_id>/refund` — Devuelve factura (admin).

## Formato de respuesta de error

Los errores devuelven un JSON uniforme:

```json
{
  "status": "error",
  "message": "Descripción del error"
}
```

## Casos importantes de prueba

- Registro con email válido -> `201`
- Registro con email duplicado -> `409`
- Login correcto -> `200`
- Login inválido -> `401`
- Crear producto sin admin -> `403`
- Checkout con carrito vacío -> `400`
- Consultar factura de otro usuario -> `403`
- Refund sin admin -> `403`

## Pruebas automáticas

Ejecuta desde `Project`:

```bash
pytest -q
```

La suite ya está validada y debería pasar con `41` tests.



