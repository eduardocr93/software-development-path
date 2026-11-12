const getPokemon = require("./getPokemon");

Promise.any([getPokemon(25), getPokemon(150), getPokemon(200)])
  .then(result => console.log("Primer Pokémon resuelto:", result.name))
  .catch(err => console.error("Error:", err));
