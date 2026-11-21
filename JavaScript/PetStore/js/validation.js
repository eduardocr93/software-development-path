export const EMAIL_PATTERN = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;

export function validateAuth(form, mode) {
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

export function readProductForm(form) {
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