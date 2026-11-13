const getPokemon = require("./getPokemon");

Promise.all([getPokemon(1), getPokemon(4), getPokemon(7)])
  .then(results => {
    results.forEach(p => console.log("Pokémon:", p.name));
  })
  .catch(err => console.error("Error:", err));
