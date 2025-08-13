# Number Trainer


Математический тренажер для изучения арифметики с поддержкой GUI, консольного и веб-интерфейса.

## Структура проекта

```
number_trainer/
├── src/
│   └── number_trainer/          # Основной пакет
│       ├── core/                # Бизнес-логика
│       │   ├── models.py        # Модели данных
│       │   └── trainer.py       # Основной класс тренажера
│       ├── gui/                 # Графический интерфейс
│       │   ├── app.py          # GUI приложение
│       │   └── styles.py       # Стили оформления
│       ├── cli/                 # Консольный интерфейс
│       │   └── console.py       # Консольная версия
│       └── web/                 # Веб-интерфейс
│           ├── app.py          # FastAPI приложение
│           ├── routes.py       # API маршруты
│           ├── models.py       # Pydantic модели
│           ├── main.py         # Точка входа веб-сервера
│           └── static/         # Статические файлы (CSS, JS)
├── tests/                       # Тесты
│   ├── test_core/              # Тесты бизнес-логики
│   ├── test_gui/               # Тесты GUI
│   └── test_web/               # Тесты веб-интерфейса
├── main.py                      # Точка входа GUI
├── demo.py                      # Демо консольной версии
└── pyproject.toml              # Конфигурация проекта
```

## Установка и запуск

Проект использует `uv` для управления зависимостями.

### Требования
- Python >= 3.8
- uv

### Быстрый старт с Taskfile
```bash
# Показать все доступные команды
task --list

# Настроить среду разработки
task dev

# Запустить GUI приложение
task run

# Запустить консольную версию
task run-console

# Запустить тесты
task test
```

### Основные команды
```bash
# 📦 УСТАНОВКА
task install         # Установить зависимости
task install-dev     # Установить dev зависимости

# 🏃 ЗАПУСК
task run             # Запустить GUI приложение
task run-console     # Запустить консольную версию
task run-web         # Запустить веб-сервер (браузерная версия)
task demo            # Показать демонстрацию

# 🧪 ТЕСТИРОВАНИЕ
task test            # Запустить тесты
task test-cov        # Тесты с покрытием кода
task test-watch      # Тесты в режиме наблюдения

# 🔧 КАЧЕСТВО КОДА
task lint            # Проверить линтерами
task format          # Отформатировать код
task ci              # Все проверки CI

# ℹ️ ИНФОРМАЦИЯ
task info            # Информация о проекте
task health          # Проверка здоровья
task help            # Подробная справка
```

### Альтернативный запуск
```bash
# GUI версия
uv run python3 main.py
uv run number-trainer

# Консольная версия
uv run python3 demo.py
uv run number-trainer-console

# Веб-версия
uv run python3 web_main.py
uv run number-trainer-web
```

## Веб-интерфейс

Веб-версия Number Trainer предоставляет современный браузерный интерфейс с адаптивным дизайном для десктопа и мобильных устройств.

### Запуск веб-сервера
```bash
task run-web
# или
uv run python3 web_main.py
```

После запуска откройте браузер и перейдите по адресу: http://localhost:8000

### Особенности веб-интерфейса
- **Адаптивный дизайн** - работает на десктопе и мобильных устройствах
- **Современный UI** - использует цветовую схему из GUI версии
- **REST API** - полноценный API для интеграции
- **Горячие клавиши** - Enter (проверить), Escape (главное меню)
- **Статистика в реальном времени** - отслеживание прогресса
- **Автопереход** - автоматический переход к следующему упражнению

### API Endpoints
- `GET /` - главная страница приложения
- `POST /api/exercise/new` - создать новое упражнение
- `POST /api/exercise/check` - проверить ответ
- `GET /api/stats` - получить статистику
- `GET /api/health` - проверка состояния сервера

## Docker

Number Trainer поддерживает запуск в Docker контейнере для упрощения развертывания и изоляции окружения.

### Быстрый старт с Docker

```bash
# Собрать и запустить с помощью Docker Compose
task docker-compose-up

# Или собрать и запустить вручную
task docker-build
task docker-run
```

### Docker команды

```bash
# 🐳 DOCKER
task docker-build           # Собрать Docker образ
task docker-run             # Запустить Docker контейнер
task docker-stop            # Остановить контейнеры
task docker-clean           # Очистить образы и контейнеры

# 🐳 DOCKER COMPOSE
task docker-compose-up      # Запустить через Docker Compose (development)
task docker-compose-down    # Остановить Docker Compose
task docker-compose-logs    # Показать логи
task docker-compose-build   # Пересобрать образ

# 🐳 PRODUCTION DOCKER
task docker-compose-prod    # Запустить в production режиме
task docker-compose-prod-down # Остановить production
task docker-compose-prod-logs # Логи production
task docker-compose-prod-build # Пересобрать production образ

# 🐳 GITHUB CONTAINER REGISTRY
task docker-build-ghcr      # Собрать для GitHub Container Registry
task docker-push-ghcr       # Опубликовать в GHCR
task docker-publish         # Собрать и опубликовать
```

### Запуск из GitHub Container Registry

```bash
# Запустить последнюю версию
docker run -p 8000:8000 ghcr.io/[username]/number-trainer:latest

# Запустить конкретную версию
docker run -p 8000:8000 ghcr.io/[username]/number-trainer:v1.0.0

# Запустить major.minor версию (последний patch)
docker run -p 8000:8000 ghcr.io/[username]/number-trainer:1.0
```

## 🚀 Web Release Instructions

### **Release Workflow**

Number Trainer использует автоматизированный процесс релизов через GitHub Actions. Docker образы публикуются только при создании версионных тегов.

#### **1. Подготовка к релизу**

```bash
# Убедитесь, что вы на main ветке
git checkout main
git pull origin main

# Проверьте текущую версию в pyproject.toml
cat pyproject.toml | grep version
```

#### **2. Обновление версии**

```bash
# Отредактируйте pyproject.toml
# Измените version = "0.1.0" на новую версию, например "1.0.0"

# Закоммитьте изменения версии
git add pyproject.toml
git commit -m "Bump version to 1.0.0"
git push origin main
```

#### **3. Создание релиза**

```bash
# Создайте тег для релиза
git tag v1.0.0

# Отправьте тег в GitHub
git push origin v1.0.0
```

#### **4. Автоматическая сборка и публикация**

После отправки тега GitHub Actions автоматически:
- ✅ Соберет Docker образ
- ✅ Протестирует его работоспособность
- ✅ Опубликует в GitHub Container Registry
- ✅ Создаст теги: `v1.0.0`, `1.0`, `latest`

#### **5. Проверка релиза**

```bash
# Проверьте, что образ доступен
docker pull ghcr.io/[username]/number-trainer:v1.0.0

# Протестируйте локально
docker run -p 8000:8000 ghcr.io/[username]/number-trainer:v1.0.0
```

### **Versioning Strategy**

#### **Semantic Versioning (SemVer)**
- `v1.0.0` - Major.Minor.Patch
- `v1.1.0` - Новые функции (minor)
- `v2.0.0` - Breaking changes (major)

#### **Available Tags**
- `latest` - Последний стабильный релиз
- `v1.0.0` - Конкретная версия
- `1.0` - Последний patch для major.minor

### **Development vs Production**

#### **Development Workflow**
```bash
# Обычная разработка
git push origin main
# → Запускает тестовую сборку (без публикации)
```

#### **Production Release**
```bash
# Релиз
git tag v1.0.0 && git push origin v1.0.0
# → Запускает production сборку и публикацию
```

### **Deployment Examples**

#### **Local Development**
```bash
# Запуск локальной версии
task docker-compose-up
```

#### **Production Deployment**
```bash
# Запуск production версии
docker run -d -p 8000:8000 \
  --name number-trainer \
  ghcr.io/[username]/number-trainer:v1.0.0
```

#### **Docker Compose Production**
```bash
# Создайте docker-compose.yml
version: '3.8'
services:
  number-trainer:
    image: ghcr.io/[username]/number-trainer:v1.0.0
    ports:
      - "8000:8000"
    restart: unless-stopped

# Запустите
docker-compose up -d
```

### **Rollback Strategy**

```bash
# Откат к предыдущей версии
docker stop number-trainer
docker run -d -p 8000:8000 \
  --name number-trainer \
  ghcr.io/[username]/number-trainer:v0.9.0
```

### **Monitoring Releases**

- **GitHub Actions**: Проверьте статус сборки в Actions tab
- **Container Registry**: Просмотрите опубликованные образы в Packages
- **Health Check**: `curl http://localhost:8000/api/health`

### **Quick Reference**

#### **Common Release Commands**
```bash
# Создать новый релиз
git tag v1.0.0 && git push origin v1.0.0

# Список всех тегов
git tag -l

# Удалить локальный тег (если нужно)
git tag -d v1.0.0

# Удалить удаленный тег (если нужно)
git push origin --delete v1.0.0
```

#### **Check Release Status**
```bash
# Проверить доступные образы
docker search ghcr.io/[username]/number-trainer

# Проверить теги образа
docker pull ghcr.io/[username]/number-trainer:latest
docker images | grep number-trainer
```

### Переменные окружения

- `PORT` - порт для запуска приложения (по умолчанию: 8000)
- `HOST` - хост для привязки (по умолчанию: 0.0.0.0)
- `WORKERS` - количество worker процессов (по умолчанию: 1, production: 4)
- `LOG_LEVEL` - уровень логирования (по умолчанию: info, production: warning)
- `PYTHONUNBUFFERED` - отключение буферизации Python (по умолчанию: 1)

### Production vs Development

**Development режим:**
- Автоперезагрузка при изменении кода
- Подробное логирование
- 1 worker процесс

**Production режим:**
- Отключена автоперезагрузка
- Оптимизированное логирование
- 4 worker процесса
- Ограничения ресурсов (CPU/Memory)
- Дополнительные меры безопасности
- Read-only файловая система (кроме временных директорий)

### Health Check

Контейнер включает health check, который проверяет доступность API:
```bash
curl http://localhost:8000/api/health
```

Ожидаемый ответ:
```json
{"status": "healthy", "service": "number-trainer-web"}
```

## Структура проекта

- `main.py` - основной файл приложения с GUI на tkinter
- `pyproject.toml` - конфигурация проекта
- `README.md` - документация

## Разработка

Приложение создано с использованием:
- **Python** - основной язык программирования
- **tkinter** - встроенная библиотека GUI для десктопной версии
- **FastAPI** - современный веб-фреймворк для API
- **uvicorn** - ASGI сервер для веб-приложения
- **HTML/CSS/JavaScript** - фронтенд веб-интерфейса
- **uv** - управление зависимостями и проектом

### Архитектура
- **Модульная структура** - разделение на core, gui, cli, web
- **Единая бизнес-логика** - все интерфейсы используют общий `MathTrainer`
- **REST API** - стандартизированное взаимодействие с веб-интерфейсом
- **Адаптивный дизайн** - поддержка десктопа и мобильных устройств