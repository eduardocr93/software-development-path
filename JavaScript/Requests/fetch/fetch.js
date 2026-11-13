import {
  createObject,
  deleteObject,
  getObjectById,
  getObjects,
  patchObject,
  replaceObject,
} from "../api.js";

const message = document.querySelector("#message");
const result = document.querySelector("#result");

function showResult(value, text) {
  message.textContent = text;
  message.classList.remove("error");
  result.textContent = JSON.stringify(value, null, 2);
}

function showError(error) {
  if (error.status === 404) {
    message.textContent = "No se encontró ningún objeto con ese ID. Verifica el ID e inténtalo de nuevo.";
  } else if (error.status === 405) {
    message.textContent = "El API no permite esta operación con ese objeto. Puede ser un ID reservado; prueba con un objeto creado por ti mediante POST.";
  } else {
    message.textContent = error.message;
  }
  message.classList.add("error");
  result.textContent = "";
}

function readData(form, allowNull = false) {
  const data = JSON.parse(new FormData(form).get("data"));
  if ((!allowNull && !data) || (data !== null && (typeof data !== "object" || Array.isArray(data)))) {
    throw new Error("Los datos deben ser un objeto JSON, por ejemplo: {\"color\":\"azul\"}.");
  }
  return data;
}

async function runRequest(action, successMessage, onSuccess) {
  try {
    const response = await action();
    onSuccess?.(response);
    const messageText = typeof successMessage === "function"
      ? successMessage(response)
      : successMessage;
    showResult(response, messageText);
  } catch (error) {
    showError(error);
  }
}

document.querySelector("#getAllButton").addEventListener("click", () => {
  runRequest(
    getObjects,
    (objects) => `Se recibieron ${objects.length} objetos. Los creados con POST se buscan por su ID.`,
  );
});

document.querySelector("#getOneForm").addEventListener("submit", (event) => {
  event.preventDefault();
  const id = new FormData(event.currentTarget).get("id").trim();
  runRequest(
    () => getObjectById(id),
    "Artículo cargado en los formularios PUT y PATCH.",
    (item) => {
      const data = JSON.stringify(item.data ?? {}, null, 2);
      const putForm = document.querySelector("#putForm");
      putForm.elements.id.value = item.id;
      putForm.elements.name.value = item.name;
      putForm.elements.data.value = data;

      const patchForm = document.querySelector("#patchForm");
      patchForm.elements.id.value = item.id;
      patchForm.elements.data.value = data;
    },
  );
});

document.querySelector("#createForm").addEventListener("submit", (event) => {
  event.preventDefault();
  const form = event.currentTarget;
  try {
    const values = new FormData(form);
    const name = values.get("name").trim();
    const data = readData(form);
    runRequest(
      () => createObject(name, data),
      "Artículo creado. Guarda su ID: lo necesitarás para consultarlo o modificarlo.",
    );
  } catch (error) {
    showError(error);
  }
});

document.querySelector("#putForm").addEventListener("submit", (event) => {
  event.preventDefault();
  const form = event.currentTarget;
  try {
    const values = new FormData(form);
    const id = values.get("id").trim();
    const name = values.get("name").trim();
    const data = readData(form, true);
    runRequest(() => replaceObject(id, name, data), "Artículo reemplazado correctamente.");
  } catch (error) {
    showError(error);
  }
});

document.querySelector("#patchForm").addEventListener("submit", (event) => {
  event.preventDefault();
  const form = event.currentTarget;
  try {
    const values = new FormData(form);
    const id = values.get("id").trim();
    const data = readData(form);
    runRequest(() => patchObject(id, data), "Datos del artículo actualizados correctamente.");
  } catch (error) {
    showError(error);
  }
});

document.querySelector("#deleteForm").addEventListener("submit", (event) => {
  event.preventDefault();
  const id = new FormData(event.currentTarget).get("id").trim();
  if (window.confirm(`¿Seguro que quieres eliminar el artículo ${id}?`)) {
    runRequest(() => deleteObject(id), "Artículo eliminado correctamente.");
  }
});
