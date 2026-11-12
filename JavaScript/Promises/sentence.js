function delayWord(word, time) {
  return new Promise(resolve => {
    setTimeout(() => {
      resolve(word);
    }, time);
  });
}

const words = ["very", "dogs", "cute", "are"];
const delays = { very: 300, dogs: 100, cute: 400, are: 200 };
const resolvedWords = [];
const promises = words.map(word => {
  return delayWord(word, delays[word]).then(resolvedWord => {
    resolvedWords.push(resolvedWord);
    return resolvedWord;
  });
});

Promise.all(promises).then(() => {
  resolvedWords[0] =
    resolvedWords[0][0].toUpperCase() + resolvedWords[0].slice(1);
  console.log(resolvedWords.join(" "));
});
