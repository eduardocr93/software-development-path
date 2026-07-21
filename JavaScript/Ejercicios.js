// Ejercicio 1: recorrer una lista e imprimir todos sus elementos
const lista = ["manzana", "banana", "cereza", "durazno"];
console.log("Ejercicio 1: imprimir elementos de la lista");
for (let i = 0; i < lista.length; i++) {
  console.log(lista[i]);
}

// Ejercicio 2: recorrer una lista de números y almacenar los pares en otra lista (con for)
const numeros = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
const paresFor = [];
for (let i = 0; i < numeros.length; i++) {
  if (numeros[i] % 2 === 0) {
    paresFor.push(numeros[i]);
  }
}
console.log("\nEjercicio 2 (for): pares encontrados:", paresFor);

// Ejercicio 3: usar filter para obtener los pares
const paresFilter = numeros.filter(numero => numero % 2 === 0);
console.log("Ejercicio 3 (filter): pares encontrados:", paresFilter);

// Ejercicio 4: convertir temperaturas de Celsius a Fahrenheit con map
const celsius = [0, 10, 20, 30, 37];
const fahrenheit = celsius.map(tempC => (tempC * 9) / 5 + 32);
console.log("\nEjercicio 4: Celsius a Fahrenheit:");
console.log("Celsius:", celsius);
console.log("Fahrenheit:", fahrenheit);

// Ejercicio 5: convertir un string en una lista de palabras sin usar split
const example = "This is a string!";
const result = [];
let palabra = "";

for (let i = 0; i < example.length; i++) {
  const caracter = example[i];
  if (caracter === " ") {
    if (palabra !== "") {
      result.push(palabra);
      palabra = "";
    }
  } else {
    palabra += caracter;
  }
}

if (palabra !== "") {
  result.push(palabra);
}

console.log("\nEjercicio 5: string a lista de palabras sin split:", result);

// Ejercicio 6: transformar datos del estudiante
const student = {
  name: "John Doe",
  grades: [
    { name: "math", grade: 80 },
    { name: "science", grade: 100 },
    { name: "history", grade: 60 },
    { name: "PE", grade: 90 },
    { name: "music", grade: 98 }
  ]
};

let total = 0;
let highest = student.grades[0];
let lowest = student.grades[0];

for (let i = 0; i < student.grades.length; i++) {
  const item = student.grades[i];
  total += item.grade;
  if (item.grade > highest.grade) {
    highest = item;
  }
  if (item.grade < lowest.grade) {
    lowest = item;
  }
}

const studentResult = {
  name: student.name,
  gradeAvg: Number((total / student.grades.length).toFixed(1)),
  highestGrade: highest.name,
  lowestGrade: lowest.name
};

console.log("\nEjercicio 6: resultado del estudiante:", studentResult);
