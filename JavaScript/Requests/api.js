const API_BASE_URL = "https://api.restful-api.dev";

async function request(path, options = {}) {
  let response;

  try {
    response = await fetch(`${API_BASE_URL}${path}`, {
      ...options,
      headers: {
        "Content-Type": "application/json",
        ...options.headers,
      },
    });
  } catch (error) {
    throw new Error(`No se pudo conectar con el API: ${error.message}`);
  }

  let result;
  try {
    result = await response.json();
  } catch {
    result = null;
  }

  if (!response.ok) {
    const message = result?.error || result?.message || response.statusText;
    const error = new Error(`Error ${response.status}: ${message || "la solicitud no fue aceptada"}`);
    error.status = response.status;
    throw error;
  }

  return result;
}

export function getObjects() {
  return request("/objects");
}

export function getObjectById(id) {
  return request(`/objects/${encodeURIComponent(id)}`);
}

export function createObject(name, data) {
  return request("/objects", {
    method: "POST",
    body: JSON.stringify({ name, data }),
  });
}

export function replaceObject(id, name, data) {
  return request(`/objects/${encodeURIComponent(id)}`, {
    method: "PUT",
    body: JSON.stringify({ name, data }),
  });
}

export function patchObject(id, data) {
  return request(`/objects/${encodeURIComponent(id)}`, {
    method: "PATCH",
    body: JSON.stringify({ data }),
  });
}

export function deleteObject(id) {
  return request(`/objects/${encodeURIComponent(id)}`, {
    method: "DELETE",
  });
}
