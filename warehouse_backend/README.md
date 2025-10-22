# Warehouse Scanner Backend API

FastAPI backend для мобільного додатку сканування товарів на складі з інтеграцією Odoo 15 Community.

## Опис

Цей backend надає REST API для мобільного Flutter додатку, який дозволяє:
- Авторизацію користувачів через Odoo
- Перевірку PIN-кодів
- Завантаження деталей накладних (stock.picking)
- Сканування товарів та оновлення кількостей
- Підтвердження замовлень
- Відміну збірки замовлень

## Вимоги

- Python 3.9+
- Odoo 15 Community Edition (з доступом до XML-RPC)
- PostgreSQL (для Odoo)

## Встановлення

### 1. Клонування репозиторію

```bash
cd /home/user/mortgage/warehouse_backend
```

### 2. Створення віртуального середовища

```bash
python3 -m venv venv
source venv/bin/activate  # На Linux/Mac
# або
venv\Scripts\activate  # На Windows
```

### 3. Встановлення залежностей

```bash
pip install -r requirements.txt
```

### 4. Налаштування змінних середовища

Скопіюйте `.env.example` в `.env` та налаштуйте:

```bash
cp .env.example .env
nano .env
```

Основні параметри:

```env
# Odoo Connection
ODOO_URL=http://localhost:8069
ODOO_DB=odoo15
ODOO_USERNAME=admin
ODOO_PASSWORD=admin

# Security - ВАЖЛИВО: змініть в production!
SECRET_KEY=your-very-secret-key-change-this-in-production

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True
```

## Запуск

### Режим розробки (з auto-reload)

```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

або

```bash
python app/main.py
```

### Режим production

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Запуск з Gunicorn (рекомендовано для production)

```bash
pip install gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## API Документація

Після запуску доступна автоматична документація:

- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc
- **OpenAPI JSON**: http://localhost:8000/api/openapi.json

## API Endpoints

### Аутентифікація

#### POST `/api/auth/login`
Авторизація користувача

**Request:**
```json
{
  "username": "admin",
  "password": "admin"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user_id": 2,
  "username": "admin",
  "name": "Administrator"
}
```

#### POST `/api/auth/verify-pin`
Перевірка PIN-коду (потребує токен)

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request:**
```json
{
  "pin": "1234"
}
```

**Response:**
```json
{
  "success": true,
  "message": "PIN verified successfully"
}
```

#### GET `/api/auth/me`
Отримати інформацію про поточного користувача

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:**
```json
{
  "id": 2,
  "username": "admin",
  "name": "Administrator",
  "email": "admin@example.com"
}
```

### Операції на складі

#### GET `/api/warehouse/orders/{order_name}`
Отримати деталі накладної за номером

**Example:** `/api/warehouse/orders/OUT/00123`

**Response:**
```json
{
  "id": 15,
  "name": "OUT/00123",
  "partner_name": "Customer Name",
  "state": "assigned",
  "lines": [
    {
      "id": 45,
      "product_id": 123,
      "product_name": "Product A",
      "barcode": "1234567890",
      "quantity_ordered": 10.0,
      "quantity_done": 0.0,
      "quantity_remaining": 10.0,
      "unit_of_measure": "Units"
    }
  ],
  "total_lines": 3,
  "completed_lines": 0,
  "scanned_count": 0,
  "total_count": 25,
  "remaining_count": 25
}
```

#### GET `/api/warehouse/orders/id/{order_id}`
Отримати деталі накладної за ID

#### POST `/api/warehouse/orders/{order_id}/scan`
Сканувати товар

**Request:**
```json
{
  "barcode": "1234567890"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Product scanned successfully",
  "scanned_count": 1,
  "remaining_count": 24,
  "total_count": 25,
  "order_completed": false
}
```

Можливі статуси:
- `success` - товар успішно відсканований
- `line_completed` - позиція повністю зібрана
- `error_extra` - зайвий товар (позиція вже виконана)
- `error_not_in_order` - товару немає в замовленні

#### POST `/api/warehouse/orders/{order_id}/confirm`
Підтвердити замовлення

**Response:**
```json
{
  "success": true,
  "message": "Order confirmed successfully",
  "tracking_number": "OUT/00123"
}
```

#### POST `/api/warehouse/orders/{order_id}/cancel`
Відмінити збірку замовлення

**Request:**
```json
{
  "order_id": 15,
  "reason": "Wrong order selected"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Order cancelled successfully"
}
```

## Інтеграція з Odoo

### Необхідні моделі Odoo

Backend використовує стандартні моделі Odoo 15:

- `res.users` - користувачі
- `stock.picking` - накладні/переміщення
- `stock.move` - рядки переміщення
- `product.product` - товари

### Додаткове поле для PIN-коду (опціонально)

Для збереження PIN-кодів користувачів, додайте в Odoo Custom модуль:

```python
# models/res_users.py
from odoo import models, fields

class ResUsers(models.Model):
    _inherit = 'res.users'

    x_pin = fields.Char(string='PIN Code', size=4)
```

Якщо поле не створено, backend приймає будь-який 4-значний PIN (для тестування).

### XML-RPC доступ

Переконайтеся, що XML-RPC увімкнено в конфігурації Odoo:

```ini
# odoo.conf
xmlrpc = True
xmlrpc_interface = 0.0.0.0
xmlrpc_port = 8069
```

## Структура проекту

```
warehouse_backend/
├── app/
│   ├── main.py                 # Головний файл FastAPI
│   ├── config.py               # Конфігурація
│   ├── models/
│   │   ├── auth.py            # Моделі аутентифікації
│   │   └── warehouse.py       # Моделі операцій на складі
│   ├── services/
│   │   ├── odoo_client.py     # Odoo XML-RPC клієнт
│   │   └── warehouse_service.py # Бізнес-логіка складу
│   ├── routers/
│   │   ├── auth.py            # Endpoints аутентифікації
│   │   └── warehouse.py       # Endpoints складу
│   └── dependencies/
│       └── auth.py            # JWT токени, залежності
├── requirements.txt
├── .env.example
└── README.md
```

## Безпека

### Production рекомендації

1. **Змініть SECRET_KEY** в `.env` на випадкову строку
2. **Налаштуйте CORS** в `app/main.py` - вкажіть конкретні домени замість `"*"`
3. **Використовуйте HTTPS** для production
4. **Налаштуйте firewall** - дозвольте доступ тільки з мобільних пристроїв
5. **Обмежте XML-RPC** - Odoo має бути доступний тільки для backend, не напряму

### Генерація SECRET_KEY

```python
import secrets
print(secrets.token_urlsafe(32))
```

## Логування

Логи записуються в stdout. Рівень логування налаштовується в `.env`:

```env
LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR, CRITICAL
```

## Тестування

### Тест з'єднання з Odoo

```bash
python -c "from app.services.odoo_client import get_odoo_client; print(get_odoo_client().uid)"
```

### Тест API з curl

```bash
# Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin"}'

# Get order (з токеном)
curl -X GET http://localhost:8000/api/warehouse/orders/OUT/00123 \
  -H "Authorization: Bearer <your_token>"
```

## Docker (опціонально)

### Dockerfile

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  backend:
    build: .
    ports:
      - "8000:8000"
    environment:
      - ODOO_URL=http://odoo:8069
      - ODOO_DB=odoo15
      - ODOO_USERNAME=admin
      - ODOO_PASSWORD=admin
    depends_on:
      - odoo
```

## Troubleshooting

### Помилка з'єднання з Odoo

```
Error: socket.gaierror: [Errno -2] Name or service not known
```

**Рішення:** Перевірте ODOO_URL в `.env`, переконайтеся що Odoo запущений

### JWT Token Invalid

```
{"detail": "Could not validate credentials"}
```

**Рішення:** Токен застарів або невірний SECRET_KEY. Отримайте новий токен через `/api/auth/login`

### PIN verification завжди повертає success=false

**Рішення:** Переконайтеся що в Odoo створено поле `x_pin` для моделі `res.users`

## Підтримка

Для питань та підтримки звертайтесь до команди розробки.

## Ліцензія

Внутрішнє використання.
