import fetch from "node-fetch";

function getPokemon(id) {
  return fetch(`https://pokeapi.co/api/v2/pokemon/${id}`)
    .then(res => res.json());
}

Promise.any([getPokemon(25), getPokemon(150), getPokemon(200)])
  .then(result => console.log("Primer Pokémon resuelto:", result.name))
  .catch(err => console.error("Error:", err));
