const API_BASE_URL = document.querySelector('meta[name="api-base"]')?.content?.replace(/\/+$/, "")
  || "http://127.0.0.1:5000";

async function request(path, { method = "GET", body, token } = {}) {
  let response;
  try {
    response = await fetch(`${API_BASE_URL}${path}`, {
      method,
      headers: {
        ...(body === undefined ? {} : { "Content-Type": "application/json" }),
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
      },
      ...(body === undefined ? {} : { body: JSON.stringify(body) }),
    });
  } catch (error) {
    throw new Error(`No se pudo conectar con el API (${API_BASE_URL}). Verifica que el backend esté activo y permita solicitudes desde este origen.`);
  }

  const contentType = response.headers.get("content-type") || "";
  const result = contentType.includes("application/json") ? await response.json() : null;
  if (!response.ok) {
    const error = new Error(result?.message || result?.error || `Error ${response.status}: ${response.statusText}`);
    error.status = response.status;
    throw error;
  }
  return result;
}

export const register = (data) => request("/auth/register", { method: "POST", body: data });
export const login = (data) => request("/auth/login", { method: "POST", body: data });
export const getProducts = () => request("/products/");
export const getProduct = (id) => request(`/products/${encodeURIComponent(id)}`);
export const getAdminInvoices = (token) => request("/invoices/admin", { token });
export const createProduct = (data, token) => request("/products/", { method: "POST", body: data, token });
export const updateProduct = (id, data, token) => request(`/products/${encodeURIComponent(id)}`, { method: "PUT", body: data, token });
export const deleteProduct = (id, token) => request(`/products/${encodeURIComponent(id)}`, { method: "DELETE", token });
export const getCart = (token) => request("/carts/my-cart", { token });
export const createCart = (token) => request("/carts/", { method: "POST", token });
export const addCartItem = (data, token) => request("/carts/items", { method: "POST", body: data, token });
export const updateCartItem = (id, data, token) => request(`/carts/items/${encodeURIComponent(id)}`, { method: "PUT", body: data, token });
export const deleteCartItem = (id, token) => request(`/carts/items/${encodeURIComponent(id)}`, { method: "DELETE", token });
export const checkout = (data, token) => request("/invoices/checkout", { method: "POST", body: data, token });
