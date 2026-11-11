const resolvedWords = [];

function delayWord(word, time) {
  return new Promise(resolve => {
    setTimeout(() => {
      resolvedWords.push(word);
      resolve();
    }, time);
  });
}

const words = [
  delayWord("very", 300),
  delayWord("Dogs", 100),
  delayWord("cute", 400),
  delayWord("are", 200),
];

Promise.all(words).then(() => {
  console.log(resolvedWords.join(" "));
});
