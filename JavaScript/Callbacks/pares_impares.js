function checkNumber(num, evenCallback, oddCallback) {
  if (num % 2 === 0) {
    evenCallback();
  } else {
    oddCallback();
  }
}

function showEvenMessage() {
  console.log("The number is even!");
}

function showOddMessage() {
  console.log("The number is odd!");
}

checkNumber(4, showEvenMessage, showOddMessage);
checkNumber(7, showEvenMessage, showOddMessage);
