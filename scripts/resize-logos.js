const sharp = require("sharp");
const path = require("path");
const fs = require("fs");

const sizes = [512, 256, 128, 64, 32, 16];
const logoSource = path.join(
  __dirname,
  "../frontend/public/images/logo/logo.png"
);
const outputDir = path.join(__dirname, "../frontend/public");

async function resizeLogos() {
  try {
    // Create resized versions
    for (const size of sizes) {
      await sharp(logoSource)
        .resize(size, size, {
          fit: "contain",
          background: { r: 0, g: 0, b: 0, alpha: 0 },
        })
        .png()
        .toFile(path.join(outputDir, `icon-${size}.png`));
      console.log(`Created icon-${size}.png`);
    }

    // Generate favicon.ico (32x32 and 16x16)
    const favicon32 = await sharp(logoSource)
      .resize(32, 32, {
        fit: "contain",
        background: { r: 0, g: 0, b: 0, alpha: 0 },
      })
      .png()
      .toBuffer();

    const favicon16 = await sharp(logoSource)
      .resize(16, 16, {
        fit: "contain",
        background: { r: 0, g: 0, b: 0, alpha: 0 },
      })
      .png()
      .toBuffer();

    // Note: For proper favicon.ico, use a library like 'to-ico'
    // For now, just create the PNG versions
    fs.writeFileSync(path.join(outputDir, "favicon-32.png"), favicon32);
    fs.writeFileSync(path.join(outputDir, "favicon-16.png"), favicon16);
    console.log("Created favicon-32.png and favicon-16.png");

    console.log("\nAll logo sizes created successfully!");
    console.log(
      "Note: For favicon.ico generation, install to-ico: npm install to-ico"
    );
  } catch (error) {
    console.error("Error resizing logos:", error);
  }
}

resizeLogos();
