const fs = require('fs');
const { createCanvas, loadImage } = require('canvas');

// SVG to PNG conversion using canvas
async function convertSVGtoPNG(svgPath, outputPath, size) {
  try {
    // Read SVG file
    const svgBuffer = fs.readFileSync(svgPath);
    const svgString = svgBuffer.toString('utf-8');
    
    // Create a data URL from the SVG
    const svgDataUrl = 'data:image/svg+xml;base64,' + Buffer.from(svgString).toString('base64');
    
    // Create canvas
    const canvas = createCanvas(size, size);
    const ctx = canvas.getContext('2d');
    
    // Load and draw the image
    const img = await loadImage(svgDataUrl);
    ctx.drawImage(img, 0, 0, size, size);
    
    // Save as PNG
    const buffer = canvas.toBuffer('image/png');
    fs.writeFileSync(outputPath, buffer);
    console.log(`✓ Generated ${outputPath} (${size}x${size})`);
  } catch (error) {
    console.error(`✗ Error generating ${outputPath}:`, error.message);
  }
}

async function generateAllLogoPNGs() {
  const logoDir = '../public/images/logo';
  const svgIconPath = `${logoDir}/roots-revealed-icon.svg`;
  
  const sizes = [
    { size: 512, name: 'icon-512x512.png' },
    { size: 256, name: 'icon-256x256.png' },
    { size: 128, name: 'icon-128x128.png' },
    { size: 64, name: 'icon-64x64.png' },
    { size: 32, name: 'favicon-32x32.png' },
    { size: 16, name: 'favicon-16x16.png' }
  ];
  
  console.log('Generating PNG logo variations...\n');
  
  // Check if SVG exists
  if (!fs.existsSync(svgIconPath)) {
    console.error(`✗ SVG file not found: ${svgIconPath}`);
    process.exit(1);
  }
  
  // Generate all sizes
  for (const { size, name } of sizes) {
    const outputPath = `${logoDir}/${name}`;
    await convertSVGtoPNG(svgIconPath, outputPath, size);
  }
  
  console.log('\n✓ All PNG variations generated successfully!');
  console.log('\nNext step: Generate favicon.ico using an online tool or imagemagick:');
  console.log('  convert icon-16x16.png icon-32x32.png icon-64x64.png favicon.ico');
}

// Run the generator
generateAllLogoPNGs().catch(error => {
  console.error('Fatal error:', error);
  process.exit(1);
});
