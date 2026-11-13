import { createObject, getObjectById, patchObject } from "./api.js";

const SESSION_KEY = "requests-user-id";
const message = document.querySelector("#message");

function showMessage(text, isError = false) {
  message.textContent = text;
  message.classList.toggle("error", isError);
}

function setBusy(form, busy) {
  const button = form.querySelector('button[type="submit"]');
  button.disabled = busy;
}

function getUserId(form) {
  return new FormData(form).get("id").trim();
}

function explainRequestError(error) {
  if (error.status === 404) {
    return "No encontramos un usuario con ese ID.";
  }
  return error.message || "Ocurrió un error al comunicarse con el API.";
}

async function register() {
  const form = document.querySelector("#registerForm");
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    setBusy(form, true);
    showMessage("Creando usuario…");

    try {
      const values = new FormData(form);
      const user = await createObject(values.get("name").trim(), {
        email: values.get("email").trim(),
        password: values.get("password"),
      });

      if (!user?.id) {
        throw new Error("El API creó la solicitud, pero no devolvió un ID de usuario.");
      }

      localStorage.setItem(SESSION_KEY, user.id);
      window.alert(`Usuario creado correctamente! Tu id es ${user.id}`);
      window.location.href = "./profile.html";
    } catch (error) {
      showMessage(explainRequestError(error), true);
    } finally {
      setBusy(form, false);
    }
  });
}

async function login() {
  const form = document.querySelector("#loginForm");
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    setBusy(form, true);
    showMessage("Verificando usuario…");

    try {
      const values = new FormData(form);
      const id = values.get("id").trim();
      const user = await getObjectById(id);

      if (user?.data?.password !== values.get("password")) {
        showMessage("El ID o la contraseña son incorrectos.", true);
        return;
      }

      localStorage.setItem(SESSION_KEY, user.id);
      window.location.href = "./profile.html";
    } catch (error) {
      showMessage(
        error.status === 404
          ? "El usuario no existe. Revisa el ID e inténtalo de nuevo."
          : explainRequestError(error),
        true,
      );
    } finally {
      setBusy(form, false);
    }
  });
}

function addProfileItem(container, title, value) {
  const card = document.createElement("article");
  card.className = "profile-item";

  const heading = document.createElement("h3");
  heading.textContent = title;
  const content = document.createElement("p");
  content.textContent = typeof value === "string" ? value : JSON.stringify(value);

  card.append(heading, content);
  container.append(card);
}

async function loadProfile() {
  const id = localStorage.getItem(SESSION_KEY);
  if (!id) {
    window.location.replace("./login.html");
    return;
  }

  const container = document.querySelector("#profile");
  try {
    const user = await getObjectById(id);
    container.replaceChildren();
    addProfileItem(container, "ID", user.id);
    addProfileItem(container, "Nombre", user.name);

    for (const [key, value] of Object.entries(user.data || {})) {
      if (key.toLowerCase() !== "password") {
        addProfileItem(container, key, value);
      }
    }
    showMessage("Perfil cargado correctamente.");
  } catch (error) {
    showMessage(explainRequestError(error), true);
  }

  document.querySelector("#logoutButton").addEventListener("click", () => {
    localStorage.removeItem(SESSION_KEY);
    window.location.href = "./login.html";
  });
}

async function changePassword() {
  const form = document.querySelector("#changePasswordForm");
  const sessionId = localStorage.getItem(SESSION_KEY);
  if (sessionId) {
    form.elements.id.value = sessionId;
  }

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const values = new FormData(form);
    const id = values.get("id").trim();
    const oldPassword = values.get("oldPassword");
    const newPassword = values.get("newPassword");
    const confirmation = values.get("confirmation");

    if (newPassword !== confirmation) {
      showMessage("La nueva contraseña y su confirmación no coinciden.", true);
      return;
    }

    setBusy(form, true);
    showMessage("Validando usuario y contraseña…");
    try {
      const user = await getObjectById(id);
      if (user?.data?.password !== oldPassword) {
        showMessage("La contraseña anterior es incorrecta.", true);
        return;
      }

      await patchObject(id, { password: newPassword });
      form.reset();
      if (sessionId) {
        form.elements.id.value = sessionId;
      }
      showMessage("La contraseña se actualizó correctamente.");
    } catch (error) {
      showMessage(explainRequestError(error), true);
    } finally {
      setBusy(form, false);
    }
  });
}

const page = document.body.dataset.page;
if (page === "register") register();
if (page === "login") login();
if (page === "profile") loadProfile();
if (page === "change-password") changePassword();
