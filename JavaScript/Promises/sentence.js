function delayWord(word, time) {
  return new Promise(resolve => {
    setTimeout(() => resolve(word), time);
  });
}

const words = [
  delayWord("dogs", 100),
  delayWord("are", 200),
  delayWord("very", 300),
  delayWord("cute", 400),
];

Promise.all(words).then(result => {
  console.log(result.join(" "));
});
