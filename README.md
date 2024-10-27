# Проект: Онлайн чат с использованием FastAPI и WebSocket

## Описание проекта
Этот проект представляет собой онлайн чат-приложение, созданное с использованием FastAPI и WebSocket. В нем реализованы функции регистрации, входа в систему, создания и управления чат-комнатами, а также отправки сообщений в режиме реального времени. Пользователи могут создавать свои чат-комнаты, искать уже существующие комнаты и общаться друг с другом в них.

## Используемые технологии
- **Backend**: FastAPI
- **Frontend**: HTML, CSS, JavaScript
- **Базы данных**: PostgreSQL
- **Docker**: для контейнеризации сервисов
- **WebSocket**: для реализации общения в реальном времени
- **Аутентификация**: JWT токены
- **Веб-сервер**: Nginx

## Установка и запуск
### Локально:
1. Убедитесь, что у вас установлены Python и PostgreSQL.
2. Клонируйте репозиторий проекта:
   ```bash
   git clone https://github.com/ваш_репозиторий
   cd ваш_проект
   ```
3. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```
4. Настройте базу данных:
   - Создайте базу данных PostgreSQL.
   - Обновите подключение в `db.py`.
5. Запустите приложение:
   ```bash
   uvicorn website.app.main:app --reload
   uvicorn chat.app.main:app --port 8001 --reload
   ```
6. Откройте браузер и перейдите на [http://127.0.0.1:8000](http://127.0.0.1:8000) для доступа к приложению.

### С использованием Docker:
1. Убедитесь, что Docker установлен.
2. Соберите и запустите контейнеры:
   ```bash
   docker-compose up --build
   ```
3. Перейдите по адресу [http://localhost](http://localhost) для доступа к приложению.

## Инструкция по использованию
- **Регистрация**: перейдите на страницу регистрации и создайте новый аккаунт, указав email, пароль и никнейм.
- **Вход**: используйте свои учетные данные для входа в систему.
- **Чат-комнаты**: создавайте новые комнаты, заходите в существующие или ищите их по названию. Можете изменить свой никнейм.
- **Общение**: отправляйте сообщения в реальном времени и получайте уведомления о действиях других пользователей в чате.

## Возможности приложения
- **Мгновенные сообщения**: Пользователи могут отправлять сообщения в реальном времени и видеть сообщения других участников.
- **Создание и управление комнатами**: Возможность создавать чат-комнаты и удалять их.
- **Уведомления**: Система уведомлений информирует пользователей о входе и выходе других участников из чата.
- **Обработка ошибок**: Автоматическое завершение сессии при истечении срока действия токена и перенаправление на страницу входа. При неправильном вводе логина или пароля высветится соответствующее сообщение. Также при возникновении ошибки регистрации выведется соответствующая информация.

---
## Приятного использования! 
При возникновении ошибок или наличии советов и предложений по "апдейтам" писать в тг @peskovv01