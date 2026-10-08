import fetch from "node-fetch";

function getPokemon(id) {
  return fetch(`https://pokeapi.co/api/v2/pokemon/${id}`)
    .then(res => res.json());
}

Promise.all([getPokemon(1), getPokemon(4), getPokemon(7)])
  .then(results => {
    results.forEach(p => console.log("Pokémon:", p.name));
  })
  .catch(err => console.error("Error:", err));
