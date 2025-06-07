(async () => {
  try {
    const stdin = await new Promise((resolve) => {
      let data = '';
      process.stdin.on('data', chunk => data += chunk);
      process.stdin.on('end', () => resolve(data));
    });

    const { url } = JSON.parse(stdin);
    const response = await fetch(url);
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const data = await response.json();
    console.log(JSON.stringify(data));
  } catch (error) {
    console.log(JSON.stringify({ 
      error: error.message,
      type: error.constructor.name 
    }));
  }
})();
