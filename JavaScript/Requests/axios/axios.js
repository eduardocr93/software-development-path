import { mergeData } from "../api.js";
import {
  fillSportsData,
  fillSportsPatch,
  filterObjectsWithData,
  formatObjectList,
  readSportsPatch,
  readSportsData,
  runRequest,
  showError,
} from "../request-ui.js";

const API_BASE_URL = "https://api.restful-api.dev/objects";

document.querySelector("#getAllButton").addEventListener("click", () => {
  runRequest(
    () => axios.get(API_BASE_URL),
    (objects) => `Se muestran ${filterObjectsWithData(objects).length} objetos con datos.`,
    undefined,
    (response) => response.data,
    formatObjectList,
  );
});

document.querySelector("#getOneForm").addEventListener("submit", (event) => {
  event.preventDefault();
  const id = new FormData(event.currentTarget).get("id").trim();
  runRequest(
    () => axios.get(`${API_BASE_URL}/${encodeURIComponent(id)}`),
    "Artículo cargado en los formularios PUT y PATCH.",
    (item) => {
      const putForm = document.querySelector("#putForm");
      putForm.elements.id.value = item.id;
      putForm.elements.name.value = item.name;
      fillSportsData(putForm, item.data);

      const patchForm = document.querySelector("#patchForm");
      patchForm.elements.id.value = item.id;
      fillSportsPatch(patchForm, item.data);
    },
    (response) => response.data,
  );
});

document.querySelector("#createForm").addEventListener("submit", (event) => {
  event.preventDefault();
  const form = event.currentTarget;
  try {
    const values = new FormData(form);
    const name = values.get("name").trim();
    const data = readSportsData(form);
    runRequest(
      () => axios.post(API_BASE_URL, { name, data }),
      "Artículo creado. Guarda su ID: lo necesitarás para consultarlo o modificarlo.",
      undefined,
      (response) => response.data,
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
    const data = readSportsData(form);
    runRequest(
      () => axios.put(`${API_BASE_URL}/${encodeURIComponent(id)}`, { name, data }),
      "Artículo reemplazado correctamente.",
      undefined,
      (response) => response.data,
    );
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
    const data = readSportsPatch(form);
    runRequest(
      async () => {
        const path = `${API_BASE_URL}/${encodeURIComponent(id)}`;
        const current = await axios.get(path);
        return axios.patch(path, { data: mergeData(current.data.data, data) });
      },
      "Datos del artículo actualizados correctamente.",
      undefined,
      (response) => response.data,
    );
  } catch (error) {
    showError(error);
  }
});

document.querySelector("#deleteForm").addEventListener("submit", (event) => {
  event.preventDefault();
  const id = new FormData(event.currentTarget).get("id").trim();
  if (window.confirm(`¿Seguro que quieres eliminar el artículo ${id}?`)) {
    runRequest(
      () => axios.delete(`${API_BASE_URL}/${encodeURIComponent(id)}`),
      "Artículo eliminado correctamente.",
      undefined,
      (response) => response.data,
    );
  }
});
