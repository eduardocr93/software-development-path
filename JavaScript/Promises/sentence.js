function delayWord(word, time) {
  return new Promise(resolve => {
    setTimeout(() => resolve(word), time);
  });
}

const words = [
  delayWord("very", 400),
  delayWord("dogs", 100),
  delayWord("cute", 600),
  delayWord("are", 200),
];

Promise.all(words).then(result => {
  const sentence = `${result[1]} ${result[3]} ${result[0]} ${result[2]}`;
  console.log(sentence); // Dogs are very cute
});
