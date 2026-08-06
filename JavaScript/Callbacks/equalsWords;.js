const fs = require('fs');

const file1 = fs.readFileSync('./Callbacks/file1.txt', 'utf8')
  .split('\n')
  .map(word => word.trim());

const file2 = fs.readFileSync('./Callbacks/file2.txt', 'utf8')
  .split('\n')
  .map(word => word.trim());

const repeatedWords = file1.filter(word => file2.includes(word));

console.log("Palabras repetidas en ambos archivos:");
console.log(repeatedWords);

console.log("\nMensaje escondido:");
console.log(repeatedWords.join(" "));
