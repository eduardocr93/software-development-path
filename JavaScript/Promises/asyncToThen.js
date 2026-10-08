import fetch from "node-fetch";

// Usuario existente
fetch("https://reqres.in/api/users/2")
  .then(res => res.json())
  .then(data => console.log("Usuario:", data.data))
  .catch(err => console.error("Error:", err))
  .finally(() => console.log("Solicitud finalizada"));

// Usuario inexistente
fetch("https://reqres.in/api/users/23")
  .then(res => {
    if (!res.ok) throw new Error("Usuario no encontrado");
    return res.json();
  })
  .then(data => console.log("Usuario:", data.data))
  .catch(err => console.error("❌ Error:", err.message))
  .finally(() => console.log("Solicitud finalizada"));
