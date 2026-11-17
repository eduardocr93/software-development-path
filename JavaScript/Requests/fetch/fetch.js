import {
  createObject,
  deleteObject,
  getObjectById,
  getObjects,
  mergeData,
  patchObject,
  replaceObject,
} from "../api.js";
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

document.querySelector("#getAllButton").addEventListener("click", () => {
  runRequest(
    getObjects,
    (objects) => `Se muestran ${filterObjectsWithData(objects).length} objetos con datos.`,
    undefined,
    (value) => value,
    formatObjectList,
  );
});

document.querySelector("#getOneForm").addEventListener("submit", (event) => {
  event.preventDefault();
  const id = new FormData(event.currentTarget).get("id").trim();
  runRequest(
    () => getObjectById(id),
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
    const data = readSportsData(form);
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
    const data = readSportsPatch(form);
    runRequest(async () => {
      const current = await getObjectById(id);
      return patchObject(id, mergeData(current.data, data));
    }, "Datos del artículo actualizados correctamente.");
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
