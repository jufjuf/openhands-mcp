const fetch = require('node-fetch');

(async () => {
  const stdin = await new Promise((resolve) => {
    let data = '';
    process.stdin.on('data', chunk => data += chunk);
    process.stdin.on('end', () => resolve(data));
  });

  const { url } = JSON.parse(stdin);
  const response = await fetch(url);
  const data = await response.json();
  console.log(JSON.stringify(data));
})();
