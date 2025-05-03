# Vue Grape Project

Веб-приложение для работы с пользователями и диагнозами.

## Требования

- Node.js (версия 16 или выше)
- npm (Node Package Manager)
- Python (версия 3.8 или выше) для backend API

## Установка и запуск

### Frontend (Vue.js)

1. Установите зависимости:
```bash
npm install
```

2. Запустите проект в режиме разработки:
```bash
npm run dev
```

Приложение будет доступно по адресу: `http://localhost:5173`

### Backend (Python Flask)

1. Перейдите в директорию backend:
```bash
cd backend
```

2. Создайте и активируйте виртуальное окружение:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/MacOS
python3 -m venv venv
source venv/bin/activate
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Запустите сервер:
```bash
python app.py
```

API будет доступно по адресу: `http://127.0.0.1:5000`

## Конфигурация

Базовый URL API можно изменить в файле `src/config/api.js`

## Основные функции

- Авторизация пользователей
- Управление пользователями и их уровнем доверия
- Просмотр и фильтрация запросов
- Статистика по диагнозам
- Экспорт данных в архив

## Recommended IDE Setup

[VSCode](https://code.visualstudio.com/) + [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (and disable Vetur).

## Type Support for `.vue` Imports in TS

TypeScript cannot handle type information for `.vue` imports by default, so we replace the `tsc` CLI with `vue-tsc` for type checking. In editors, we need [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) to make the TypeScript language service aware of `.vue` types.

## Customize configuration

See [Vite Configuration Reference](https://vite.dev/config/).

## Project Setup

```sh
npm install
```

### Compile and Hot-Reload for Development

```sh
npm run dev
```

### Type-Check, Compile and Minify for Production

```sh
npm run build
```
