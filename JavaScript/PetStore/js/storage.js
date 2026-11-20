const SESSION_KEY = "lyfter-petstore-session";
const CART_KEY = "lyfter-petstore-cart";
const ORDER_KEY = "lyfter-petstore-last-order";

export function getSession() {
  const raw = localStorage.getItem(SESSION_KEY);
  return raw ? JSON.parse(raw) : null;
}

export function saveSession(session) {
  localStorage.setItem(SESSION_KEY, JSON.stringify(session));
}

export function clearSession() {
  localStorage.removeItem(SESSION_KEY);
}

export function getSavedCart() {
  const raw = localStorage.getItem(CART_KEY);
  return raw ? JSON.parse(raw) : null;
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
  const raw = localStorage.getItem(ORDER_KEY);
  return raw ? JSON.parse(raw) : null;
}
