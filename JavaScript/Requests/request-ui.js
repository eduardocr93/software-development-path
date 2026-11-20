const message = document.querySelector("#message");
const result = document.querySelector("#result");

export function showResult(value, text) {
  message.textContent = text;
  message.classList.remove("error");
  result.textContent = typeof value === "string" ? value : JSON.stringify(value, null, 2);
}

export function showError(error) {
  const status = error.status ?? error.response?.status;
  const serverMessage = error.response?.data?.error || error.response?.data?.message;

  if (status === 404) {
    message.textContent = "No se encontró ningún objeto con ese ID. Verifica el ID e inténtalo de nuevo.";
  } else if (status === 405) {
    message.textContent = "El API no permite esta operación con ese objeto. Puede ser un ID reservado; prueba con un objeto creado por ti mediante POST.";
  } else if (serverMessage) {
    message.textContent = `Error ${status}: ${serverMessage}`;
  } else {
    message.textContent = error.message || "Ocurrió un error al procesar la solicitud.";
  }

  message.classList.add("error");
  result.textContent = "";
}

export function readSportsData(form) {
  const values = new FormData(form);
  const brand = values.get("brand").trim();
  const type = values.get("type").trim();
  const material = values.get("material").trim();
  const sport = values.get("sport").trim();
  const priceText = values.get("price").trim();
  const price = Number(priceText);

  if (!brand || !type || !material || !sport || priceText === "" || !Number.isFinite(price) || price < 0) {
    throw new Error("Completa los cinco atributos del artículo y usa un precio válido de cero o más.");
  }

  return { brand, type, price, material, sport };
}

export function fillSportsData(form, data = {}) {
  data = data ?? {};
  form.elements.brand.value = data.brand ?? "";
  form.elements.type.value = data.type ?? "";
  form.elements.price.value = data.price ?? "";
  form.elements.material.value = data.material ?? "";
  form.elements.sport.value = data.sport ?? "";
}

export function readSportsPatch(form) {
  const values = new FormData(form);
  const updates = {};

  for (const field of ["brand", "type", "material", "sport"]) {
    const value = values.get(field).trim();
    if (value) {
      updates[field] = value;
    }
  }

  const priceText = values.get("price").trim();
  if (priceText) {
    const price = Number(priceText);
    if (!Number.isFinite(price) || price < 0) {
      throw new Error("El precio debe ser un número válido de cero o más.");
    }
    updates.price = price;
  }

  if (Object.keys(updates).length === 0) {
    throw new Error("Completa al menos un atributo que quieras actualizar.");
  }

  return updates;
}

export function fillSportsPatch(form, data = {}) {
  data = data ?? {};
  for (const field of ["brand", "type", "price", "material", "sport"]) {
    const input = form.elements[field];
    input.value = "";
    input.placeholder = data[field] == null ? "Dejar sin cambios" : `Actual: ${data[field]}`;
  }
}

export function filterObjectsWithData(objects) {
  return objects.filter((item) => item?.data != null);
}

export function formatObjectList(objects) {
  const itemsWithData = filterObjectsWithData(objects);
  if (itemsWithData.length === 0) {
    return "No se encontraron objetos con datos.";
  }

  return itemsWithData.map((item) => {
    const attributes = item.data && typeof item.data === "object" && !Array.isArray(item.data)
      ? Object.entries(item.data)
        .map(([key, value]) => `${key}: ${typeof value === "string" ? value : JSON.stringify(value)}`)
        .join(" | ") || "Sin atributos"
      : JSON.stringify(item.data);
    return `${item.name || "Objeto sin nombre"} (ID: ${item.id})\n${attributes}`;
  }).join("\n\n");
}

export async function runRequest(action, successMessage, onSuccess, unwrapResponse = (value) => value, formatResult = (value) => value) {
  try {
    const response = unwrapResponse(await action());
    onSuccess?.(response);
    const text = typeof successMessage === "function" ? successMessage(response) : successMessage;
    showResult(formatResult(response), text);
  } catch (error) {
    showError(error);
  }
}