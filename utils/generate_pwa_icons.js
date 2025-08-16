const sharp = require('sharp');
const fs = require('fs');
const path = require('path');

// Размеры иконок для PWA
const iconSizes = [
  { size: 72, name: 'icon-72.png' },
  { size: 96, name: 'icon-96.png' },
  { size: 128, name: 'icon-128.png' },
  { size: 144, name: 'icon-144.png' },
  { size: 152, name: 'icon-152.png' },
  { size: 192, name: 'icon-192.png' },
  { size: 384, name: 'icon-384.png' },
  { size: 512, name: 'icon-512.png' }
];

// Функция для генерации иконок
async function generatePWAIcons(svgPath, outputDir = './icons') {
  try {
    // Создаем папку для иконок если её нет
    if (!fs.existsSync(outputDir)) {
      fs.mkdirSync(outputDir, { recursive: true });
    }

    console.log('Генерируем PNG иконки из SVG...');

    // Генерируем иконки для каждого размера
    for (const icon of iconSizes) {
      const outputPath = path.join(outputDir, icon.name);

      await sharp(svgPath)
        .resize(icon.size, icon.size, {
          fit: 'contain',
          background: { r: 0, g: 0, b: 0, alpha: 0 } // Прозрачный фон
        })
        .png()
        .toFile(outputPath);

      console.log(`✓ Создана иконка: ${icon.name} (${icon.size}x${icon.size})`);
    }

    console.log('\n🎉 Все иконки успешно созданы!');

    // Генерируем пример manifest.json
    generateManifestExample(outputDir);

  } catch (error) {
    console.error('Ошибка при генерации иконок:', error);
  }
}

// Функция для создания примера manifest.json
function generateManifestExample(outputDir) {
  const manifest = {
    "name": "My PWA App",
    "short_name": "PWA App",
    "theme_color": "#000000",
    "background_color": "#ffffff",
    "display": "standalone",
    "start_url": "/",
    "icons": iconSizes.map(icon => ({
      "src": `icons/${icon.name}`,
      "sizes": `${icon.size}x${icon.size}`,
      "type": "image/png",
      "purpose": "any maskable"
    }))
  };

  const manifestPath = path.join(outputDir, '..', 'manifest.json');
  fs.writeFileSync(manifestPath, JSON.stringify(manifest, null, 2));
  console.log('📄 Создан пример manifest.json');
}

// Использование скрипта
const svgFilePath = process.argv[2] || './icon.svg';
const outputDirectory = process.argv[3] || './icons';

// Проверяем существование SVG файла
if (!fs.existsSync(svgFilePath)) {
  console.error(`❌ SVG файл не найден: ${svgFilePath}`);
  console.log('Использование: node generate-pwa-icons.js <путь-к-svg> [папка-вывода]');
  process.exit(1);
}

// Запускаем генерацию
generatePWAIcons(svgFilePath, outputDirectory);
