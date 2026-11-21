const SESSION_KEY = "lyfter-petstore-session";
const CART_KEY = "lyfter-petstore-cart";
const ORDER_KEY = "lyfter-petstore-last-order";

function readStoredValue(key, isValid) {
  const raw = localStorage.getItem(key);
  if (!raw) return null;

  try {
    const value = JSON.parse(raw);
    if (!isValid(value)) throw new Error("Invalid stored value");
    return value;
  } catch {
    localStorage.removeItem(key);
    return null;
  }
}

export function getSession() {
  return readStoredValue(SESSION_KEY, (value) => (
    value !== null
    && typeof value === "object"
    && !Array.isArray(value)
    && typeof value.token === "string"
    && value.token.length > 0
  ));
}

export function saveSession(session) {
  localStorage.setItem(SESSION_KEY, JSON.stringify(session));
}

export function clearSession() {
  localStorage.removeItem(SESSION_KEY);
}

export function getSavedCart() {
  return readStoredValue(CART_KEY, (value) => (
    value !== null && typeof value === "object" && !Array.isArray(value) && Array.isArray(value.items)
  ));
}

export function saveCart(cart) {
  localStorage.setItem(CART_KEY, JSON.stringify(cart));
}

export function clearCart() {
  localStorage.removeItem(CART_KEY);
}

export function saveLastOrder(order) {
  localStorage.setItem(ORDER_KEY, JSON.stringify(order));
}

export function getLastOrder() {
  return readStoredValue(ORDER_KEY, (value) => (
    value !== null
    && typeof value === "object"
    && !Array.isArray(value)
    && Array.isArray(value.items)
    && (value.invoice_id != null || typeof value.invoice_number === "string")
  ));
}
