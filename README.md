# ChatGPT Telegram bot

## Установка и запуск

### Клонируем репозиторий
```
git clone https://github.com/dodocheck/chatgpt_tg_bot.git
```

### В корневой папке создаем файл `.env` и добавляем в него переменные окружения:
```.env
TG_TOKEN=ваш_телеграм_токен
AI_TOKEN=ваш_ai_токен
PROXY=http://логин:пароль@IP:порт
```

### Запуск
```bash
docker-compose up -d
```
