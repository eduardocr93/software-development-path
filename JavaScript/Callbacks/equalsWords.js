const fs = require('fs');

fs.readFile('./Callbacks/file1.txt', 'utf8', (err, data1) => {
  if (err) {
    console.error("Error leyendo file1:", err);
    return;
  }

  const file1 = data1.split('\n').map(word => word.trim());

  fs.readFile('./Callbacks/file2.txt', 'utf8', (err, data2) => {
    if (err) {
      console.error("Error leyendo file2:", err);
      return;
    }

    const file2 = data2.split('\n').map(word => word.trim());

    const repeatedWords = file1.filter(word => file2.includes(word));

    console.log("Palabras repetidas en ambos archivos:");
    console.log(repeatedWords);

    console.log("\nMensaje escondido:");
    console.log(repeatedWords.join(" "));
  });
});