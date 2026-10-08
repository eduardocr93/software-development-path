import fetch from "node-fetch";

async function getUser() {
  try {
    const response = await fetch("https://reqres.in/api/users/2");
    const data = await response.json();
    console.log("Usuario encontrado:", data.data);
  } catch (error) {
    console.error("Error en la solicitud:", error);
  }
}

getUser();