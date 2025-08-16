# PWA Icons

## Current Icons

### Primary Icon
**`math_training_icon.svg`** - основная векторная иконка
- **Формат:** SVG (векторная графика)
- **Использование:** PWA manifest, favicon, основная иконка
- **Дизайн:** Мозг с очками в фиолетово-синих тонах

### Generated PNG Icons
**Полный набор PNG иконок созданных из SVG источника:**
- `icon-72.png` - Android (72x72)
- `icon-96.png` - Android (96x96)
- `icon-128.png` - Chrome App (128x128)
- `icon-144.png` - Windows Tile (144x144)
- `icon-152.png` - iPad (152x152)
- `icon-192.png` - Android Chrome (192x192)
- `icon-384.png` - Android Chrome (384x384)
- `icon-512.png` - Splash Screen (512x512)

## Icon Generation

**Автоматическая генерация из SVG:**
```bash
task generate-icons
```

Эта команда:
1. Настраивает Node.js окружение (`task setup-node`)
2. Устанавливает зависимости (`npm install sharp`)
3. Запускает генератор иконок из SVG в PNG

## Пути к иконкам

```
/static/icons/math_training_icon.svg    # Основная SVG
/static/icons/icon-*.png               # Генерированные PNG (72-512px)
/favicon.ico                           # Автоматически → SVG
/apple-touch-icon.png                  # Автоматически → icon-152.png
```

## Использование в коде

### Manifest.json
```json
{
  "icons": [
    {
      "src": "/static/icons/math_training_icon.svg",
      "sizes": "any",
      "type": "image/svg+xml",
      "purpose": "any maskable"
    }
  ]
}
```

### HTML мета-теги
```html
<link rel="icon" type="image/svg+xml" href="/static/icons/math_training_icon.svg">
<link rel="apple-touch-icon" href="/static/icons/math_training_icon.svg">
```

### Service Worker
```javascript
const STATIC_ASSETS = [
  '/static/icons/math_training_icon.svg',
  // другие файлы...
];
```

## Преимущества SVG иконки

- **Масштабируемость:** Идеальное качество на любом размере
- **Размер файла:** Компактная (менее 2KB)
- **Поддержка:** Современные браузеры и PWA
- **Производительность:** Быстрая загрузка и кэширование

## Замена иконки

Для замены иконки:
1. Сохраните новую SVG как `math_training_icon.svg`
2. Проверьте что viewBox настроен корректно
3. Убедитесь что SVG оптимизирована для PWA
