# Lyfter Pet Store — Frontend

Frontend en HTML, CSS y JavaScript sin dependencias de interfaz. Consume el API Flask de `Flask/project`.

## Ejecutar localmente

1. Inicia el backend desde `Flask/project`:

   ```sh
   python app.py
   ```

   El API debe estar disponible en `http://127.0.0.1:5000`.

2. Desde esta carpeta, inicia un servidor estático:

   ```sh
   python -m http.server 8765
   ```

3. Abre `http://127.0.0.1:8765`.

El backend permite por defecto los orígenes `localhost` y `127.0.0.1` en los puertos `8765` y `5500`. Para otro host o puerto, configura `FRONTEND_ORIGINS` en el entorno del backend. La URL del API se puede cambiar en el elemento `meta[name="api-base"]` de `index.html`.

## Funcionalidades

- Inicio, registro, inicio/cierre de sesión y control de rol basado en el token JWT.
- Catálogo con búsqueda, filtro de stock, detalle y estado vacío.
- Carrito remoto sincronizado con el backend y respaldo del estado en `localStorage`.
- Checkout con validación y pantalla de compra finalizada.
- Administración protegida de inventario: crear, editar y eliminar productos.
- Resumen de ventas recientes para administradores, cargado desde el endpoint protegido del API.
- Mensajes de error visibles y validación de formularios.

Para habilitar el panel, registra una cuenta y sigue las instrucciones `promote-admin` del README del backend. Luego cierra sesión e inicia sesión de nuevo para renovar el token con el rol de administrador.
