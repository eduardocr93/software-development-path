import * as api from "./api.js";
import {
  clearCart,
  clearSession,
  getLastOrder,
  getSavedCart,
  getSession,
  saveCart,
  saveLastOrder,
  saveSession,
} from "./storage.js";

const app = document.querySelector("#app");
const header = document.querySelector("#site-header");
const toastRegion = document.querySelector("#toast-region");
const EMAIL_PATTERN = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
const currency = new Intl.NumberFormat("es-CR", { style: "currency", currency: "CRC", maximumFractionDigits: 0 });

function escapeHTML(value = "") {
  return String(value).replace(/[&<>"']/g, (character) => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#39;",
  })[character]);
}

function formatPrice(value) {
  return currency.format(Number(value) || 0);
}

function formatDate(value) {
  const date = new Date(value);
  return Number.isNaN(date.getTime())
    ? "—"
    : new Intl.DateTimeFormat("es-CR", { dateStyle: "medium" }).format(date);
}

function productIcon(product) {
  const text = `${product.category || ""} ${product.name || ""}`.toLowerCase();
  if (/gato|cat/.test(text)) return "🐈";
  if (/perro|dog|can/.test(text)) return "🐕";
  if (/alimento|comida|food/.test(text)) return "🥣";
  if (/juguete|toy/.test(text)) return "🧸";
  if (/cama|descanso|bed/.test(text)) return "🛏️";
  if (/salud|cuidado|higiene/.test(text)) return "🧴";
  return "🐾";
}

function showToast(message, kind = "success") {
  toastRegion.innerHTML = `<div class="toast toast-${kind}" role="status">${escapeHTML(message)}</div>`;
  window.clearTimeout(showToast.timeout);
  showToast.timeout = window.setTimeout(() => { toastRegion.replaceChildren(); }, 4200);
}

function updateHeader() {
  const session = getSession();
  const cart = getSavedCart();
  const count = cart?.items?.reduce((total, item) => total + Number(item.quantity || 0), 0) || 0;
  header.innerHTML = `
    <div class="header-inner">
      <a class="brand" href="#home" aria-label="Lyfter Pet Store, inicio">
        <span class="brand-mark">✿</span><span>Lyfter <strong>Pet Store</strong></span>
      </a>
      <button class="menu-toggle" type="button" aria-label="Abrir navegación" aria-expanded="false">☰</button>
      <nav class="main-nav" aria-label="Navegación principal">
        <a href="#home">Inicio</a>
        <a href="#products">Productos</a>
        ${session ? `<a href="#cart">Carrito <span class="cart-count">${count}</span></a>` : ""}
        ${session?.role === "admin" ? '<a href="#admin">Administración</a>' : ""}
      </nav>
      <div class="header-account">
        ${session
          ? `<span class="account-name">${escapeHTML(session.name || session.email || "Mi cuenta")}</span><button class="text-button" type="button" data-action="logout">Salir</button>`
          : '<a class="button button-small" href="#login">Ingresar</a>'}
      </div>
    </div>`;
}

function layout(content, className = "") {
  app.className = `page-shell ${className}`.trim();
  app.innerHTML = content;
  app.focus({ preventScroll: true });
}

function showError(error) {
  if (error?.status === 401) {
    clearSession();
    updateHeader();
    showToast("Tu sesión venció. Vuelve a ingresar para continuar.", "error");
    if (location.hash !== "#login") location.hash = "#login";
    return;
  }
  showToast(error?.message || "Ocurrió un error inesperado.", "error");
}

function routeError(error, back = "#products") {
  if (error?.status === 401) {
    showError(error);
    return;
  }
  layout(`
    <section class="notice-card">
      <span class="notice-icon">!</span>
      <h1>No pudimos completar la solicitud</h1>
      <p>${escapeHTML(error?.message || "Ocurrió un error inesperado.")}</p>
      <a class="button" href="${back}">Volver</a>
    </section>`);
}

function requireSession({ admin = false } = {}) {
  const session = getSession();
  if (!session) {
    showToast("Inicia sesión para continuar.", "error");
    location.hash = "#login";
    return null;
  }
  if (admin && session.role !== "admin") {
    showToast("Esta sección es exclusiva para administradores.", "error");
    location.hash = "#home";
    return null;
  }
  return session;
}

function renderHome() {
  layout(`
    <section class="hero">
      <div class="hero-copy">
        <span class="eyebrow">Todo para una vida feliz juntos</span>
        <h1>Pequeños cuidados.<br><span>Grandes momentos.</span></h1>
        <p>Encuentra alimentos, juguetes y esenciales seleccionados para acompañar cada aventura de tu mascota.</p>
        <div class="hero-actions">
          <a class="button" href="#products">Explorar productos <span aria-hidden="true">→</span></a>
          <a class="button button-quiet" href="#about">Conócenos</a>
        </div>
        <div class="hero-trust"><span>♡</span> Cuidado pensado para toda la familia</div>
      </div>
      <div class="hero-art" aria-label="Ilustración de mascotas" role="img">
        <span class="sun-shape"></span><span class="hero-pet hero-dog">🐕</span>
        <span class="hero-pet hero-cat">🐈</span><span class="floating-toy">🎾</span>
        <span class="art-caption">Bienvenidos, amigos peludos</span>
      </div>
    </section>
    <section class="benefits" aria-label="Beneficios">
      <article><span>🌿</span><div><h2>Selección de calidad</h2><p>Productos que nos encantan para ellos.</p></div></article>
      <article><span>📦</span><div><h2>Compra sencilla</h2><p>Todo lo que necesitas, en un solo lugar.</p></div></article>
      <article><span>💛</span><div><h2>Amor en cada detalle</h2><p>Porque se merecen lo mejor de nosotros.</p></div></article>
    </section>
    <section class="home-bottom">
      <div><span class="eyebrow">Nos mueve su felicidad</span><h2>Una tienda hecha con amor por las mascotas</h2></div>
      <a class="button button-outline" href="#products">Descubrir la tienda</a>
    </section>
    <section class="about-anchor" id="about"><p>Lyfter Pet Store</p><p>Un espacio para consentir, cuidar y celebrar a quienes siempre están a nuestro lado.</p></section>`);
}

function renderAuth(mode) {
  const registering = mode === "register";
  const session = getSession();
  if (session) {
    location.hash = session.role === "admin" ? "#admin" : "#products";
    return;
  }
  layout(`
    <section class="auth-layout">
      <div class="auth-aside">
        <span class="eyebrow">${registering ? "Hola, nuevo amigo" : "Qué bueno verte de nuevo"}</span>
        <h1>${registering ? "Un hogar para todo lo que amas." : "Su próximo favorito está aquí."}</h1>
        <p>${registering ? "Crea tu cuenta para guardar tu carrito y hacer tus compras con facilidad." : "Ingresa y continúa descubriendo productos para consentir a tu mascota."}</p>
        <div class="auth-illustration" aria-hidden="true">🐶 <span>♡</span> 🐱</div>
      </div>
      <form class="form-card auth-form" id="${registering ? "register-form" : "login-form"}" novalidate>
        <span class="eyebrow">${registering ? "Únete a la familia" : "Tu cuenta"}</span>
        <h2>${registering ? "Crear cuenta" : "Iniciar sesión"}</h2>
        ${registering ? field("name", "Nombre completo", "text", "Tu nombre", { autocomplete: "name", minLength: 2, maxLength: 100 }) : ""}
        ${field("email", "Correo electrónico", "email", "nombre@ejemplo.com", { autocomplete: "email" })}
        ${field("password", "Contraseña", "password", registering ? "Al menos 6 caracteres" : "Tu contraseña", { autocomplete: registering ? "new-password" : "current-password", minLength: 6 })}
        ${registering ? field("confirmation", "Confirmar contraseña", "password", "Repite tu contraseña", { autocomplete: "new-password", minLength: 6 }) : ""}
        <p class="form-message" data-form-message aria-live="polite"></p>
        <button class="button button-full" type="submit">${registering ? "Crear mi cuenta" : "Ingresar"}</button>
        <p class="form-switch">${registering ? "¿Ya tienes una cuenta?" : "¿Primera vez por aquí?"}
          <a href="${registering ? "#login" : "#register"}">${registering ? "Inicia sesión" : "Regístrate"}</a>
        </p>
      </form>
    </section>`, "auth-page");
}

function field(name, label, type, placeholder, options = {}) {
  const attrs = [
    options.autocomplete ? `autocomplete="${options.autocomplete}"` : "",
    options.minLength ? `minlength="${options.minLength}"` : "",
    options.maxLength ? `maxlength="${options.maxLength}"` : "",
    type === "email" ? 'inputmode="email"' : "",
  ].filter(Boolean).join(" ");
  return `<label class="field">${label}<input name="${name}" type="${type}" placeholder="${placeholder}" ${attrs} required></label>`;
}

function renderProducts(products = null) {
  const session = getSession();
  layout(`
    <section class="section-heading">
      <div><span class="eyebrow">La tienda</span><h1>Catálogo para colitas felices</h1><p>Encuentra algo especial para tu compañero de aventuras.</p></div>
    </section>
    <section class="catalog-toolbar">
      <label class="search-field"><span aria-hidden="true">⌕</span><input id="product-search" type="search" placeholder="Buscar un producto…" aria-label="Buscar productos"></label>
      <label class="checkbox-field"><input id="available-only" type="checkbox"> Mostrar solo disponibles</label>
      <span class="catalog-count" id="catalog-count"></span>
    </section>
    <div class="product-grid" id="product-grid" aria-live="polite"></div>`);
  if (products === null) return;
  const grid = document.querySelector("#product-grid");
  grid.innerHTML = products.length
    ? products.map((product) => productCard(product, session)).join("")
    : emptyState("🐾", "Todavía no hay productos", "Estamos preparando el catálogo. Vuelve pronto.");
  filterProducts();
}

function productCard(product) {
  const outOfStock = Number(product.stock) < 1;
  const category = product.category || "Favoritos";
  return `<article class="product-card">
    <a class="product-visual ${outOfStock ? "is-unavailable" : ""}" href="#product/${encodeURIComponent(product.id)}" aria-label="Ver ${escapeHTML(product.name)}">
      <span class="product-category">${escapeHTML(category)}</span><span class="product-emoji" aria-hidden="true">${productIcon(product)}</span>
      <span class="visual-doodle" aria-hidden="true">✦</span>
    </a>
    <div class="product-info">
      <h2><a href="#product/${encodeURIComponent(product.id)}">${escapeHTML(product.name || "Producto")}</a></h2>
      <p class="product-description">${escapeHTML(product.description || "Un detalle especial para tu mascota.")}</p>
      <div class="product-card-bottom"><span class="price">${formatPrice(product.price)}</span>
        <span class="stock ${outOfStock ? "stock-out" : ""}">${outOfStock ? "Agotado" : `${Number(product.stock)} disponibles`}</span></div>
      <a class="button button-full button-small" href="#product/${encodeURIComponent(product.id)}">Ver detalles <span aria-hidden="true">→</span></a>
    </div>
  </article>`;
}

function filterProducts() {
  const search = document.querySelector("#product-search");
  const available = document.querySelector("#available-only");
  const grid = document.querySelector("#product-grid");
  if (!search || !grid) return;
  const query = search.value.trim().toLocaleLowerCase();
  let visibleCount = 0;
  grid.querySelectorAll(".product-card").forEach((card) => {
    const matchesText = card.textContent.toLocaleLowerCase().includes(query);
    const matchesStock = !available.checked || Number(card.dataset.stock) > 0;
    card.hidden = !matchesText || !matchesStock;
    if (!card.hidden) visibleCount += 1;
  });
  const count = document.querySelector("#catalog-count");
  if (count) count.textContent = `${visibleCount} ${visibleCount === 1 ? "producto" : "productos"}`;
  if (!visibleCount && grid.querySelector(".product-card")) {
    grid.insertAdjacentHTML("beforeend", '<p class="empty-inline" data-filter-empty>No encontramos coincidencias. Prueba con otra búsqueda.</p>');
  } else {
    grid.querySelector("[data-filter-empty]")?.remove();
  }
}

function emptyState(icon, heading, description, href = "#products", action = "Ver productos") {
  return `<section class="empty-state"><span class="empty-icon" aria-hidden="true">${icon}</span><h2>${heading}</h2><p>${description}</p><a class="button button-outline" href="${href}">${action}</a></section>`;
}

async function loadProducts() {
  renderProducts();
  try {
    const products = await api.getProducts();
    renderProducts(Array.isArray(products) ? products : []);
    document.querySelectorAll(".product-card").forEach((card, index) => {
      card.dataset.stock = String(products[index]?.stock ?? 0);
    });
  } catch (error) {
    routeError(error);
  }
}

async function loadProduct(id) {
  layout('<p class="loading-state">Cargando producto…</p>');
  try {
    const product = await api.getProduct(id);
    const stockText = Number(product.stock) > 0 ? `${Number(product.stock)} disponibles` : "Agotado por ahora";
    layout(`
      <a class="back-link" href="#products">← Volver al catálogo</a>
      <section class="product-detail">
        <div class="detail-visual"><span>${productIcon(product)}</span><small>${escapeHTML(product.category || "Favoritos")}</small></div>
        <div class="detail-copy">
          <span class="eyebrow">${escapeHTML(product.category || "Lyfter Pet Store")}</span>
          <h1>${escapeHTML(product.name || "Producto")}</h1>
          <p class="detail-price">${formatPrice(product.price)}</p>
          <p class="detail-description">${escapeHTML(product.description || "Un detalle especial para tu mascota, elegido con mucho cariño.")}</p>
          <p class="stock-detail">${Number(product.stock) > 0 ? "●" : "○"} ${stockText}</p>
          <div class="detail-actions">
            <label class="quantity-field">Cantidad <input id="detail-quantity" type="number" min="1" max="${Math.max(1, Number(product.stock) || 1)}" value="1" ${Number(product.stock) < 1 ? "disabled" : ""}></label>
            <button class="button" type="button" data-add-product="${escapeHTML(product.id)}" ${Number(product.stock) < 1 ? "disabled" : ""}>Agregar al carrito</button>
          </div>
          <p class="detail-note">Una compra sencilla para hacerlos felices todos los días.</p>
        </div>
      </section>`);
  } catch (error) {
    routeError(error);
  }
}

async function ensureCart(session) {
  try {
    return await api.getCart(session.token);
  } catch (error) {
    if (error.status !== 404) throw error;
    await api.createCart(session.token);
    return api.getCart(session.token);
  }
}

async function addToCart(productId, quantity = 1) {
  const session = requireSession();
  if (!session) return;
  const parsedQuantity = Number(quantity);
  if (!Number.isInteger(parsedQuantity) || parsedQuantity < 1) {
    showToast("La cantidad debe ser un número entero mayor a cero.", "error");
    return;
  }
  try {
    await ensureCart(session);
    await api.addCartItem({ product_id: Number(productId), quantity: parsedQuantity }, session.token);
    const updatedCart = await api.getCart(session.token);
    saveCart(updatedCart);
    updateHeader();
    showToast("Producto agregado al carrito.");
    location.hash = "#cart";
  } catch (error) {
    showError(error);
  }
}

async function loadCart() {
  const session = requireSession();
  if (!session) return;
  layout('<p class="loading-state">Cargando tu carrito…</p>');
  let cart;
  try {
    cart = await api.getCart(session.token);
  } catch (error) {
    if (error.status === 404) {
      cart = { items: [], total: 0 };
    } else {
      routeError(error, "#products");
      return;
    }
  }
  saveCart(cart);
  updateHeader();
  if (!cart.items?.length) {
    layout(`${emptyState("🛍️", "Tu carrito está esperando", "Agrega productos del catálogo y aquí aparecerán tus favoritos.", "#products", "Explorar productos")}`);
    return;
  }
  layout(`
    <section class="section-heading cart-heading"><div><span class="eyebrow">Tu selección</span><h1>Carrito de compras</h1><p>Revisa tus productos antes de continuar.</p></div></section>
    <section class="cart-layout">
      <div class="cart-items">${cart.items.map(cartItemCard).join("")}</div>
      <aside class="summary-card">
        <span class="eyebrow">Casi listo</span><h2>Resumen del pedido</h2>
        <div class="summary-line"><span>Productos (${cart.items.reduce((sum, item) => sum + Number(item.quantity), 0)})</span><strong>${formatPrice(cart.total)}</strong></div>
        <div class="summary-line"><span>Envío</span><strong>Se coordina después</strong></div>
        <div class="summary-total"><span>Total</span><strong>${formatPrice(cart.total)}</strong></div>
        <a class="button button-full" href="#checkout">Continuar al checkout <span aria-hidden="true">→</span></a>
        <a class="button button-quiet button-full" href="#products">Seguir comprando</a>
      </aside>
    </section>`);
}

function cartItemCard(item) {
  return `<article class="cart-item">
    <div class="cart-item-icon" aria-hidden="true">${productIcon({ name: item.product_name })}</div>
    <div class="cart-item-name"><h2>${escapeHTML(item.product_name)}</h2><p>${formatPrice(item.price)} c/u</p></div>
    <div class="quantity-controls" aria-label="Cantidad">
      <button type="button" aria-label="Disminuir cantidad" data-cart-action="decrease" data-item-id="${item.item_id}" data-quantity="${item.quantity}">−</button>
      <span>${Number(item.quantity)}</span>
      <button type="button" aria-label="Aumentar cantidad" data-cart-action="increase" data-item-id="${item.item_id}" data-quantity="${item.quantity}">+</button>
    </div>
    <strong class="cart-subtotal">${formatPrice(item.subtotal)}</strong>
    <button class="remove-button" type="button" data-cart-action="remove" data-item-id="${item.item_id}">Quitar</button>
  </article>`;
}

async function changeCart(action, itemId, currentQuantity) {
  const session = requireSession();
  if (!session) return;
  try {
    if (action === "remove") {
      await api.deleteCartItem(itemId, session.token);
    } else {
      const quantity = Number(currentQuantity) + (action === "increase" ? 1 : -1);
      if (quantity < 1) {
        await api.deleteCartItem(itemId, session.token);
      } else {
        await api.updateCartItem(itemId, { quantity }, session.token);
      }
    }
    await loadCart();
  } catch (error) {
    showError(error);
  }
}

async function loadCheckout() {
  const session = requireSession();
  if (!session) return;
  let cart;
  try {
    cart = await api.getCart(session.token);
  } catch (error) {
    if (error.status === 404) cart = { items: [], total: 0 };
    else {
      routeError(error, "#cart");
      return;
    }
  }
  saveCart(cart);
  if (!cart.items?.length) {
    showToast("Agrega al menos un producto antes de continuar.", "error");
    location.hash = "#cart";
    return;
  }
  layout(`
    <a class="back-link" href="#cart">← Regresar al carrito</a>
    <section class="section-heading"><div><span class="eyebrow">Un último paso</span><h1>Resumen del pedido</h1><p>Confirma tus datos para preparar la compra.</p></div></section>
    <section class="checkout-layout">
      <form class="form-card checkout-form" id="checkout-form" novalidate>
        <span class="eyebrow">Entrega</span><h2>Información de compra</h2>
        <label class="field">Nombre completo<input name="name" value="${escapeHTML(session.name || "")}" minlength="2" maxlength="100" autocomplete="name" required></label>
        <label class="field">Correo electrónico<input name="email" type="email" value="${escapeHTML(session.email || "")}" autocomplete="email" required></label>
        <label class="field">Dirección de entrega<textarea name="billing_address" minlength="5" maxlength="255" rows="3" placeholder="Provincia, cantón, distrito y señas" required></textarea></label>
        <label class="field">Método de pago<select name="payment_method" required><option value="">Selecciona un método</option><option value="SINPE">SINPE Móvil</option><option value="Tarjeta">Tarjeta</option><option value="Transferencia">Transferencia bancaria</option></select></label>
        <p class="form-message" data-form-message aria-live="polite"></p>
        <p class="fine-print">El pago se procesará de acuerdo con las opciones disponibles en la tienda.</p>
        <button class="button button-full" type="submit">Confirmar compra <span aria-hidden="true">→</span></button>
      </form>
      <aside class="summary-card checkout-summary"><span class="eyebrow">Tu compra</span><h2>Artículos seleccionados</h2>
        <div class="order-lines">${cart.items.map((item) => `<div class="order-line"><span>${escapeHTML(item.product_name)} <small>× ${Number(item.quantity)}</small></span><strong>${formatPrice(item.subtotal)}</strong></div>`).join("")}</div>
        <div class="summary-total"><span>Total</span><strong>${formatPrice(cart.total)}</strong></div>
      </aside>
    </section>`);
}

async function loadSuccess() {
  const order = getLastOrder();
  if (!order) {
    layout(`${emptyState("🐾", "No hay una compra reciente", "Cuando completes una compra, encontrarás aquí el resumen.", "#products", "Volver al catálogo")}`);
    return;
  }
  layout(`
    <section class="success-card">
      <span class="success-icon" aria-hidden="true">✓</span><span class="eyebrow">Gracias por tu compra</span>
      <h1>¡Compra realizada con éxito!</h1>
      <p>Tu pedido <strong>${escapeHTML(order.invoice_number || `#${order.invoice_id}`)}</strong> ha sido procesado.</p>
    </section>
    <section class="order-card"><div class="order-card-heading"><div><span class="eyebrow">Todo en orden</span><h2>Resumen de la compra</h2></div><span class="order-status">Confirmada</span></div>
      <div class="order-table-wrap"><table class="data-table"><thead><tr><th>Producto</th><th>Cantidad</th><th>Precio unitario</th><th>Subtotal</th></tr></thead>
      <tbody>${(order.items || []).map((item) => `<tr><td>${escapeHTML(item.product_name)}</td><td>${Number(item.quantity)}</td><td>${formatPrice(item.price ?? item.unit_price)}</td><td>${formatPrice(item.subtotal)}</td></tr>`).join("")}</tbody>
      <tfoot><tr><th colspan="3">Total</th><th>${formatPrice(order.total)}</th></tr></tfoot></table></div>
      <p class="fine-print">Entrega: ${escapeHTML(order.billing_address || "La dirección indicada durante el checkout.")} · Pago: ${escapeHTML(order.payment_method || "Confirmado")}</p>
    </section>
    <div class="success-actions"><a class="button" href="#products">Volver al catálogo</a><a class="button button-outline" href="#home">Ir al inicio</a></div>`);
}

async function loadAdmin() {
  const session = requireSession({ admin: true });
  if (!session) return;
  layout('<p class="loading-state">Cargando inventario…</p>');
  try {
    const [products, invoices] = await Promise.all([
      api.getProducts(),
      api.getAdminInvoices(session.token),
    ]);
    const totalSales = invoices.reduce((sum, invoice) => sum + Number(invoice.total || 0), 0);
    layout(`
      <section class="section-heading admin-heading"><div><span class="eyebrow">Espacio de gestión</span><h1>Administración</h1><p>Controla el catálogo y revisa el estado del inventario.</p></div></section>
      <section class="admin-stats"><article><span>Productos en catálogo</span><strong>${products.length}</strong></article><article><span>Unidades disponibles</span><strong>${products.reduce((sum, item) => sum + (Number(item.stock) || 0), 0)}</strong></article><article><span>Ventas registradas</span><strong>${invoices.length}</strong></article><article><span>Total vendido</span><strong>${formatPrice(totalSales)}</strong></article></section>
      <section class="admin-panel"><div class="panel-heading"><div><span class="eyebrow">Inventario</span><h2>Productos</h2></div><a class="button button-small" href="#admin/new">+ Agregar producto</a></div>
        ${products.length ? `<div class="table-wrap"><table class="data-table"><thead><tr><th>Producto</th><th>Categoría</th><th>Precio</th><th>Stock</th><th>Acciones</th></tr></thead><tbody>${products.map((product) => `<tr><td><strong>${escapeHTML(product.name)}</strong><small class="table-description">${escapeHTML(product.description || "")}</small></td><td>${escapeHTML(product.category || "—")}</td><td>${formatPrice(product.price)}</td><td><span class="stock-pill ${Number(product.stock) < 1 ? "stock-pill-out" : ""}">${Number(product.stock)}</span></td><td><div class="table-actions"><a class="button button-outline button-small" href="#admin/edit/${encodeURIComponent(product.id)}">Editar</a><button class="button button-danger button-small" data-delete-product="${escapeHTML(product.id)}" type="button">Eliminar</button></div></td></tr>`).join("")}</tbody></table></div>` : emptyState("🐾", "El inventario está vacío", "Agrega el primer producto para iniciar el catálogo.", "#admin/new", "Agregar producto")}
      </section>
      <section class="admin-panel sales-panel"><div class="panel-heading"><div><span class="eyebrow">Actividad de la tienda</span><h2>Ventas recientes</h2></div></div>
        <div class="table-wrap"><table class="data-table"><thead><tr><th>Pedido</th><th>Cliente</th><th>Fecha</th><th>Total</th><th>Estado</th></tr></thead><tbody>${invoices.length ? invoices.map((invoice) => `<tr><td><strong>${escapeHTML(invoice.invoice_number)}</strong></td><td>${escapeHTML(invoice.customer_name)}</td><td>${formatDate(invoice.created_at)}</td><td>${formatPrice(invoice.total)}</td><td><span class="stock-pill ${invoice.status === "REFUNDED" ? "stock-pill-out" : ""}">${escapeHTML(invoice.status)}</span></td></tr>`).join("") : '<tr><td colspan="5"><div class="api-limitation"><strong>Aún no hay ventas registradas.</strong><span>Las compras completadas aparecerán aquí.</span></div></td></tr>'}</tbody></table></div>
      </section>`);
  } catch (error) {
    routeError(error, "#home");
  }
}

async function loadProductForm(id = null) {
  const session = requireSession({ admin: true });
  if (!session) return;
  let product = null;
  if (id) {
    try {
      product = await api.getProduct(id);
    } catch (error) {
      routeError(error, "#admin");
      return;
    }
  }
  const editing = Boolean(product);
  layout(`
    <a class="back-link" href="#admin">← Volver a administración</a>
    <section class="form-page"><div class="section-heading"><div><span class="eyebrow">Inventario</span><h1>${editing ? "Editar producto" : "Agregar producto"}</h1><p>${editing ? "Actualiza la información y guarda los cambios." : "Completa los datos para incluirlo en el catálogo."}</p></div></div>
      <form id="product-form" class="form-card product-form" novalidate data-product-id="${editing ? escapeHTML(product.id) : ""}">
        ${field("name", "Nombre", "text", "Ej. Juguete resistente", { minLength: 2, maxLength: 100 })}
        <label class="field">Descripción<textarea name="description" rows="4" maxlength="2000" placeholder="Cuéntanos qué hace especial a este producto"></textarea></label>
        ${field("price", "Precio (₡)", "number", "0", {})}
        ${field("category", "Categoría", "text", "Ej. Juguetes", { maxLength: 100 })}
        ${field("stock", "Unidades disponibles", "number", "0", {})}
        <p class="form-message" data-form-message aria-live="polite"></p>
        <div class="form-actions"><a class="button button-quiet" href="#admin">Cancelar</a><button class="button" type="submit">${editing ? "Guardar cambios" : "Crear producto"}</button></div>
      </form>
    </section>`);
  const form = document.querySelector("#product-form");
  if (product) {
    form.elements.name.value = product.name || "";
    form.elements.description.value = product.description || "";
    form.elements.price.value = product.price ?? "";
    form.elements.category.value = product.category || "";
    form.elements.stock.value = product.stock ?? 0;
  }
  form.elements.price.min = "0";
  form.elements.price.step = "0.01";
  form.elements.stock.min = "0";
  form.elements.stock.step = "1";
}

function currentRoute() {
  const [route, ...parts] = location.hash.replace(/^#\/?/, "").split("/");
  return { route: route || "home", parts: parts.map((part) => decodeURIComponent(part)) };
}

async function renderRoute() {
  updateHeader();
  const { route, parts } = currentRoute();
  if (route === "home") return renderHome();
  if (route === "about") {
    await renderHome();
    document.querySelector("#about")?.scrollIntoView({ behavior: "smooth", block: "start" });
    return;
  }
  if (route === "login" || route === "register") return renderAuth(route);
  if (route === "products") return loadProducts();
  if (route === "product" && parts[0]) return loadProduct(parts[0]);
  if (route === "cart") return loadCart();
  if (route === "checkout") return loadCheckout();
  if (route === "success") return loadSuccess();
  if (route === "admin" && parts[0] === "edit" && parts[1]) return loadProductForm(parts[1]);
  if (route === "admin" && parts[0] === "new") return loadProductForm();
  if (route === "admin") return loadAdmin();
  layout(`${emptyState("🐾", "No encontramos esa página", "La dirección puede haber cambiado.", "#home", "Volver al inicio")}`);
}

function setFormMessage(form, message, isError = false) {
  const node = form.querySelector("[data-form-message]");
  if (!node) return;
  node.textContent = message;
  node.classList.toggle("message-error", isError);
  node.classList.toggle("message-success", !isError && Boolean(message));
}

function setBusy(form, busy) {
  const button = form.querySelector('button[type="submit"]');
  if (button) {
    button.disabled = busy;
    button.dataset.originalText ||= button.textContent;
    button.textContent = busy ? "Procesando…" : button.dataset.originalText;
  }
}

function validateAuth(form, mode) {
  const values = new FormData(form);
  const name = String(values.get("name") || "").trim();
  const email = String(values.get("email") || "").trim();
  const password = String(values.get("password") || "");
  if (mode === "register" && (name.length < 2 || name.length > 100)) return "El nombre debe tener entre 2 y 100 caracteres.";
  if (!EMAIL_PATTERN.test(email) || email.length > 255) return "Ingresa un correo electrónico válido.";
  if (password.length < 6) return "La contraseña debe tener al menos 6 caracteres.";
  if (mode === "register" && values.get("confirmation") !== password) return "Las contraseñas no coinciden.";
  return null;
}

function decodeToken(token) {
  try {
    const segment = token.split(".")[1];
    if (!segment) throw new Error("Token JWT inválido");
    const encoded = segment.replace(/-/g, "+").replace(/_/g, "/");
    return JSON.parse(atob(encoded.padEnd(Math.ceil(encoded.length / 4) * 4, "=")));
  } catch {
    throw new Error("El API respondió con un token de sesión inválido. Intenta iniciar sesión de nuevo.");
  }
}

async function submitAuth(form, mode) {
  const issue = validateAuth(form, mode);
  if (issue) {
    setFormMessage(form, issue, true);
    return;
  }
  setBusy(form, true);
  setFormMessage(form, mode === "register" ? "Creando tu cuenta…" : "Verificando tus datos…");
  const values = new FormData(form);
  const name = String(values.get("name") || "").trim();
  const email = String(values.get("email") || "").trim();
  try {
    if (mode === "register") {
      await api.register({ name, email, password: values.get("password") });
      setFormMessage(form, "Tu cuenta se creó. Ahora puedes iniciar sesión.");
      window.setTimeout(() => { location.hash = "#login"; }, 800);
      return;
    }
    const response = await api.login({ email, password: values.get("password") });
    if (!response?.access_token) throw new Error("El API no devolvió un token de acceso.");
    const claims = decodeToken(response.access_token);
    saveSession({
      token: response.access_token,
      role: claims.role || "client",
      userId: claims.sub || "",
      name: name || email.split("@")[0],
      email,
    });
    updateHeader();
    showToast("¡Bienvenido a Lyfter Pet Store!");
    location.hash = claims.role === "admin" ? "#admin" : "#products";
  } catch (error) {
    setFormMessage(form, error.message, true);
  } finally {
    setBusy(form, false);
  }
}

function readProductForm(form) {
  const values = new FormData(form);
  const name = String(values.get("name") || "").trim();
  const description = String(values.get("description") || "").trim();
  const category = String(values.get("category") || "").trim();
  const priceText = String(values.get("price") || "").trim();
  const stockText = String(values.get("stock") || "").trim();
  const price = Number(priceText);
  const stock = Number(stockText);
  if (name.length < 2 || name.length > 100) throw new Error("El nombre debe tener entre 2 y 100 caracteres.");
  if (priceText === "" || !Number.isFinite(price) || price < 0) throw new Error("El precio debe ser un número igual o mayor a cero.");
  if (stockText === "" || !Number.isInteger(stock) || stock < 0) throw new Error("El stock debe ser un entero igual o mayor a cero.");
  if (category.length > 100) throw new Error("La categoría no puede superar los 100 caracteres.");
  return { name, description, price, stock, category };
}

async function submitProduct(form) {
  try {
    const data = readProductForm(form);
    const session = requireSession({ admin: true });
    if (!session) return;
    setBusy(form, true);
    setFormMessage(form, "Guardando producto…");
    if (form.dataset.productId) {
      await api.updateProduct(form.dataset.productId, data, session.token);
      showToast("Los cambios se guardaron correctamente.");
    } else {
      await api.createProduct(data, session.token);
      showToast("El producto se agregó al catálogo.");
    }
    location.hash = "#admin";
  } catch (error) {
    if (error instanceof Error && !error.status) setFormMessage(form, error.message, true);
    else showError(error);
  } finally {
    setBusy(form, false);
  }
}

async function submitCheckout(form) {
  const values = new FormData(form);
  const name = String(values.get("name") || "").trim();
  const email = String(values.get("email") || "").trim();
  const billingAddress = String(values.get("billing_address") || "").trim();
  const paymentMethod = String(values.get("payment_method") || "");
  if (name.length < 2 || name.length > 100) return setFormMessage(form, "El nombre debe tener entre 2 y 100 caracteres.", true);
  if (!EMAIL_PATTERN.test(email) || email.length > 255) return setFormMessage(form, "Ingresa un correo electrónico válido.", true);
  if (billingAddress.length < 5 || billingAddress.length > 255) return setFormMessage(form, "La dirección debe tener entre 5 y 255 caracteres.", true);
  if (!paymentMethod) return setFormMessage(form, "Selecciona un método de pago.", true);
  const session = requireSession();
  if (!session) return;
  setBusy(form, true);
  setFormMessage(form, "Confirmando tu compra…");
  try {
    const cart = await api.getCart(session.token);
    const result = await api.checkout({ billing_address: billingAddress, payment_method: paymentMethod }, session.token);
    saveLastOrder({
      invoice_id: result.invoice_id,
      invoice_number: result.invoice_number,
      billing_address: billingAddress,
      payment_method: paymentMethod,
      total: cart.total,
      items: cart.items,
    });
    clearCart();
    updateHeader();
    location.hash = `#success/${result.invoice_id}`;
  } catch (error) {
    setFormMessage(form, error.message, true);
  } finally {
    setBusy(form, false);
  }
}

document.addEventListener("submit", (event) => {
  const form = event.target;
  if (!(form instanceof HTMLFormElement)) return;
  event.preventDefault();
  if (form.id === "login-form") submitAuth(form, "login");
  if (form.id === "register-form") submitAuth(form, "register");
  if (form.id === "product-form") submitProduct(form);
  if (form.id === "checkout-form") submitCheckout(form);
});

document.addEventListener("click", async (event) => {
  const menuButton = event.target.closest(".menu-toggle");
  if (menuButton) {
    const nav = header.querySelector(".main-nav");
    const expanded = menuButton.getAttribute("aria-expanded") === "true";
    menuButton.setAttribute("aria-expanded", String(!expanded));
    nav.classList.toggle("nav-open", !expanded);
    return;
  }
  const logoutButton = event.target.closest('[data-action="logout"]');
  if (logoutButton) {
    clearSession();
    updateHeader();
    showToast("Has cerrado sesión.");
    location.hash = "#home";
    return;
  }
  const addButton = event.target.closest("[data-add-product]");
  if (addButton) {
    const quantity = document.querySelector("#detail-quantity")?.value || "1";
    await addToCart(addButton.dataset.addProduct, quantity);
    return;
  }
  const cartButton = event.target.closest("[data-cart-action]");
  if (cartButton) {
    await changeCart(cartButton.dataset.cartAction, cartButton.dataset.itemId, cartButton.dataset.quantity);
    return;
  }
  const deleteButton = event.target.closest("[data-delete-product]");
  if (deleteButton) {
    const session = requireSession({ admin: true });
    if (!session || !window.confirm("¿Eliminar este producto del catálogo?")) return;
    deleteButton.disabled = true;
    try {
      await api.deleteProduct(deleteButton.dataset.deleteProduct, session.token);
      showToast("El producto se eliminó.");
      await loadAdmin();
    } catch (error) {
      deleteButton.disabled = false;
      showError(error);
    }
  }
});

document.addEventListener("input", (event) => {
  if (event.target.id === "product-search") filterProducts();
});
document.addEventListener("change", (event) => {
  if (event.target.id === "available-only") filterProducts();
});
window.addEventListener("hashchange", renderRoute);
if (!location.hash) location.hash = "#home";
renderRoute();
