export function field(name, label, type, placeholder, options = {}) {
  const attributes = [
    options.autocomplete ? `autocomplete="${options.autocomplete}"` : "",
    options.minLength ? `minlength="${options.minLength}"` : "",
    options.maxLength ? `maxlength="${options.maxLength}"` : "",
    options.min !== undefined ? `min="${options.min}"` : "",
    options.step !== undefined ? `step="${options.step}"` : "",
    type === "email" ? 'inputmode="email"' : "",
  ].filter(Boolean).join(" ");
  return `<label class="field">${label}<input name="${name}" type="${type}" placeholder="${placeholder}" ${attributes} required></label>`;
}

export function productCard(product, { escapeHTML, formatPrice, productIcon }) {
  const outOfStock = Number(product.stock) < 1;
  const category = product.category || "Favoritos";
  return `<article class="product-card" data-stock="${Number(product.stock) || 0}">
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

export function cartItemCard(item, { escapeHTML, formatPrice, productIcon }) {
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

export function productRow(product, { escapeHTML, formatPrice }) {
  return `<tr>
    <td><strong>${escapeHTML(product.name)}</strong><small class="table-description">${escapeHTML(product.description || "")}</small></td>
    <td>${escapeHTML(product.category || "—")}</td>
    <td>${formatPrice(product.price)}</td>
    <td><span class="stock-pill ${Number(product.stock) < 1 ? "stock-pill-out" : ""}">${Number(product.stock)}</span></td>
    <td><div class="table-actions">
      <a class="button button-outline button-small" href="#admin/edit/${encodeURIComponent(product.id)}">Editar</a>
      <button class="button button-danger button-small" data-delete-product="${escapeHTML(product.id)}" type="button">Eliminar</button>
    </div></td>
  </tr>`;
}

export function invoiceRow(invoice, { escapeHTML, formatDate, formatPrice }) {
  return `<tr>
    <td><strong>${escapeHTML(invoice.invoice_number)}</strong></td>
    <td>${escapeHTML(invoice.customer_name)}</td>
    <td>${formatDate(invoice.created_at)}</td>
    <td>${formatPrice(invoice.total)}</td>
    <td><span class="stock-pill ${invoice.status === "REFUNDED" ? "stock-pill-out" : ""}">${escapeHTML(invoice.status)}</span></td>
  </tr>`;
}