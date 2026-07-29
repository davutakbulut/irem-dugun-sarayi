const fs = require('fs');
const babel = require('@babel/core');

try {
  const html = fs.readFileSync('index.html', 'utf8');
  const scriptRegex = /<script type="text\/babel">([\s\S]*?)<\/script>/g;
  let match;
  let count = 0;
  while ((match = scriptRegex.exec(html)) !== null) {
    count++;
    const jsCode = match[1];
    console.log(`Checking Babel Script #${count}...`);
    try {
      babel.transformSync(jsCode, {
        presets: ['@babel/preset-react']
      });
      console.log(`Script #${count} syntax OK!`);
    } catch (err) {
      console.error(`Syntax Error in Script #${count}:`, err.message);
    }
  }
} catch (e) {
  console.error(e);
}
