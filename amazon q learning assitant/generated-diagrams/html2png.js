const puppeteer = require('puppeteer');
const path = require('path');

(async () => {
  try {
    // Launch a headless browser
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    
    // Set viewport size
    await page.setViewport({ width: 850, height: 1100 });
    
    // Get the absolute path to the HTML file
    const htmlPath = path.resolve(__dirname, 'creative_diagram.html');
    const fileUrl = `file://${htmlPath}`;
    
    // Navigate to the HTML file
    await page.goto(fileUrl, { waitUntil: 'networkidle0' });
    
    // Take a screenshot
    await page.screenshot({ 
      path: path.resolve(__dirname, 'aws_learning_assistant_creative_html.png'),
      fullPage: true
    });
    
    // Close the browser
    await browser.close();
    
    console.log('Screenshot saved successfully!');
  } catch (error) {
    console.error('Error generating screenshot:', error);
  }
})();
