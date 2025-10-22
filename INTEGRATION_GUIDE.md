# Warehouse Scanner - Integration Guide

Інструкція по інтеграції Flutter мобільного додатку з FastAPI backend та Odoo 15.

## Архітектура системи

```
┌─────────────────────┐
│  Flutter Mobile App │
│   (warehouse_       │
│   scanner_app)      │
└──────────┬──────────┘
           │ HTTPS/REST API
           │ JWT Auth
           ▼
┌─────────────────────┐
│  FastAPI Backend    │
│   (warehouse_       │
│   backend)          │
└──────────┬──────────┘
           │ XML-RPC
           │ Internal Network
           ▼
┌─────────────────────┐
│   Odoo 15 Server    │
│   Community Edition │
└─────────────────────┘
```

## Компоненти проекту

### 1. Flutter Mobile App (`warehouse_scanner_app/`)

**Локація:** `/home/user/mortgage/warehouse_scanner_app/`

**Технології:**
- Flutter 3.0+
- Provider (state management)
- SharedPreferences (local storage)

**Статус:** ✅ Готовий (потребує інтеграції з backend)

### 2. FastAPI Backend (`warehouse_backend/`)

**Локація:** `/home/user/mortgage/warehouse_backend/`

**Технології:**
- FastAPI 0.104+
- JWT Authentication
- Odoo XML-RPC Client
- Pydantic models

**Статус:** ✅ Готовий

### 3. HTML Demo (`docs/`)

**Локація:** `/home/user/mortgage/docs/`

**Призначення:** Статичні HTML прототипи екранів для демонстрації

**Статус:** ✅ Готовий (GitHub Pages: https://finintra.github.io/mortgage/)

## Крок 1: Налаштування Odoo 15

### 1.1 Встановлення Odoo (якщо ще не встановлено)

```bash
# Через Docker (найпростіший спосіб)
docker run -d \
  -e POSTGRES_USER=odoo \
  -e POSTGRES_PASSWORD=odoo \
  -e POSTGRES_DB=postgres \
  --name db postgres:13

docker run -d \
  -p 8069:8069 \
  --name odoo \
  --link db:db \
  -e HOST=db \
  -e USER=odoo \
  -e PASSWORD=odoo \
  odoo:15
```

### 1.2 Створення тестових даних

1. Відкрийте Odoo: http://localhost:8069
2. Створіть базу даних `odoo15`
3. Встановіть модулі: `stock`, `sale`
4. Створіть тестові дані:
   - Товари з баркодами
   - Замовлення на продаж
   - Накладні (Delivery Orders) зі статусом "Ready"

### 1.3 Додавання поля PIN для користувачів (опціонально)

Створіть Custom модуль або додайте через Developer Mode:

**Settings → Technical → Database Structure → Models**
- Модель: `res.users`
- Додайте поле: `x_pin` (Char, size=4)

Встановіть PIN для тестового користувача.

## Крок 2: Запуск Backend API

### 2.1 Встановлення залежностей

```bash
cd /home/user/mortgage/warehouse_backend

# Створити віртуальне середовище
python3 -m venv venv
source venv/bin/activate

# Встановити пакети
pip install -r requirements.txt
```

### 2.2 Налаштування конфігурації

```bash
# Копіювати приклад конфігурації
cp .env.example .env

# Редагувати .env
nano .env
```

**Важливі параметри в `.env`:**

```env
# Odoo з'єднання
ODOO_URL=http://localhost:8069
ODOO_DB=odoo15
ODOO_USERNAME=admin
ODOO_PASSWORD=admin

# Безпека - ЗМІНІТЬ в production!
SECRET_KEY=your-random-secret-key-here

# API
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True
```

### 2.3 Запуск backend

```bash
# Через run.sh скрипт
./run.sh

# Або напряму
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Перевірка:**
- API Docs: http://localhost:8000/api/docs
- Health check: http://localhost:8000/api/health

### 2.4 Тестування backend

```bash
# Тест логіну
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin"}'

# Відповідь:
# {
#   "access_token": "eyJhbGc...",
#   "token_type": "bearer",
#   "user_id": 2,
#   "username": "admin",
#   "name": "Administrator"
# }
```

## Крок 3: Інтеграція Flutter з Backend

### 3.1 Додавання HTTP залежності

Відредагуйте `warehouse_scanner_app/pubspec.yaml`:

```yaml
dependencies:
  flutter:
    sdk: flutter
  provider: ^6.1.1
  shared_preferences: ^2.2.2
  http: ^1.1.0  # ДОДАТИ ЦЕЙ РЯДОК
```

Виконайте:

```bash
cd /home/user/mortgage/warehouse_scanner_app
flutter pub get
```

### 3.2 Створення API клієнта

Створіть файл `lib/services/api_client.dart`:

```dart
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

class ApiClient {
  // ЗМІНІТЬ на вашу IP адресу backend сервера
  static const String baseUrl = 'http://192.168.1.100:8000/api';

  String? _token;

  // Встановити токен
  void setToken(String token) {
    _token = token;
  }

  // Отримати токен
  String? get token => _token;

  // Headers з авторизацією
  Map<String, String> get _headers {
    final headers = {
      'Content-Type': 'application/json',
    };
    if (_token != null) {
      headers['Authorization'] = 'Bearer $_token';
    }
    return headers;
  }

  // Login
  Future<Map<String, dynamic>> login(String username, String password) async {
    final response = await http.post(
      Uri.parse('$baseUrl/auth/login'),
      headers: {'Content-Type': 'application/json'},
      body: json.encode({
        'username': username,
        'password': password,
      }),
    );

    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      _token = data['access_token'];

      // Зберегти токен локально
      final prefs = await SharedPreferences.getInstance();
      await prefs.setString('access_token', _token!);

      return data;
    } else {
      throw Exception('Login failed: ${response.body}');
    }
  }

  // Verify PIN
  Future<Map<String, dynamic>> verifyPin(String pin) async {
    final response = await http.post(
      Uri.parse('$baseUrl/auth/verify-pin'),
      headers: _headers,
      body: json.encode({'pin': pin}),
    );

    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else {
      throw Exception('PIN verification failed');
    }
  }

  // Get order by name
  Future<Map<String, dynamic>> getOrder(String orderName) async {
    final response = await http.get(
      Uri.parse('$baseUrl/warehouse/orders/$orderName'),
      headers: _headers,
    );

    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else {
      throw Exception('Order not found');
    }
  }

  // Scan product
  Future<Map<String, dynamic>> scanProduct(int orderId, String barcode) async {
    final response = await http.post(
      Uri.parse('$baseUrl/warehouse/orders/$orderId/scan'),
      headers: _headers,
      body: json.encode({'barcode': barcode}),
    );

    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else {
      throw Exception('Scan failed');
    }
  }

  // Confirm order
  Future<Map<String, dynamic>> confirmOrder(int orderId) async {
    final response = await http.post(
      Uri.parse('$baseUrl/warehouse/orders/$orderId/confirm'),
      headers: _headers,
    );

    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else {
      throw Exception('Confirm failed');
    }
  }

  // Cancel order
  Future<Map<String, dynamic>> cancelOrder(int orderId, String? reason) async {
    final response = await http.post(
      Uri.parse('$baseUrl/warehouse/orders/$orderId/cancel'),
      headers: _headers,
      body: json.encode({
        'order_id': orderId,
        'reason': reason,
      }),
    );

    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else {
      throw Exception('Cancel failed');
    }
  }
}
```

### 3.3 Оновлення AppState

Відредагуйте `lib/providers/app_state.dart`, замініть TODO на реальні API виклики:

```dart
import 'package:warehouse_scanner_app/services/api_client.dart';

class AppState extends ChangeNotifier {
  final ApiClient _api = ApiClient();

  String _currentUser = '';
  String _currentOrder = '';
  int _currentOrderId = 0;
  // ... інші поля

  // Авторизація
  Future<bool> login(String username, String password) async {
    try {
      final result = await _api.login(username, password);
      _currentUser = result['username'];

      final prefs = await SharedPreferences.getInstance();
      await prefs.setString('current_user', username);

      notifyListeners();
      return true;
    } catch (e) {
      print('Login error: $e');
      return false;
    }
  }

  // Перевірка PIN
  Future<bool> verifyPin(String pin) async {
    try {
      final result = await _api.verifyPin(pin);
      return result['success'] == true;
    } catch (e) {
      print('PIN error: $e');
      return false;
    }
  }

  // Скан накладної
  Future<void> scanInvoice(String invoiceNumber) async {
    try {
      final order = await _api.getOrder(invoiceNumber);

      _currentOrder = order['name'];
      _currentOrderId = order['id'];
      _totalCount = order['total_count'];
      _scannedCount = order['scanned_count'];
      _remainingCount = order['remaining_count'];

      notifyListeners();
    } catch (e) {
      print('Invoice scan error: $e');
      throw e;
    }
  }

  // Скан товару
  Future<String> scanProduct(String barcode) async {
    try {
      final result = await _api.scanProduct(_currentOrderId, barcode);

      _scannedCount = result['scanned_count'];
      _remainingCount = result['remaining_count'];

      notifyListeners();

      return result['status']; // success, line_completed, error_extra, etc.
    } catch (e) {
      print('Product scan error: $e');
      return 'error';
    }
  }

  // Підтвердження замовлення
  Future<void> confirmOrder() async {
    try {
      await _api.confirmOrder(_currentOrderId);

      // Очистка даних
      _currentOrder = '';
      _currentOrderId = 0;
      _scannedCount = 0;
      _totalCount = 0;
      _remainingCount = 0;

      notifyListeners();
    } catch (e) {
      print('Confirm error: $e');
      throw e;
    }
  }

  // Відміна збірки
  Future<void> cancelPicking() async {
    try {
      await _api.cancelOrder(_currentOrderId, null);

      // Очистка даних
      _currentOrder = '';
      _currentOrderId = 0;
      _scannedCount = 0;
      _totalCount = 0;
      _remainingCount = 0;

      notifyListeners();
    } catch (e) {
      print('Cancel error: $e');
      throw e;
    }
  }
}
```

### 3.4 Налаштування IP адреси backend

**ВАЖЛИВО:** В `api_client.dart` змініть `baseUrl`:

```dart
// Для локальної розробки (емулятор Android)
static const String baseUrl = 'http://10.0.2.2:8000/api';

// Для реального пристрою (знайдіть IP вашого комп'ютера)
static const String baseUrl = 'http://192.168.1.100:8000/api';

// Для production
static const String baseUrl = 'https://api.yourcompany.com/api';
```

**Як знайти вашу IP адресу:**

```bash
# Linux/Mac
ifconfig | grep "inet "

# Windows
ipconfig
```

## Крок 4: Тестування системи

### 4.1 Запуск всього

```bash
# Термінал 1: Odoo (якщо через Docker)
docker start db odoo

# Термінал 2: Backend
cd /home/user/mortgage/warehouse_backend
source venv/bin/activate
./run.sh

# Термінал 3: Flutter
cd /home/user/mortgage/warehouse_scanner_app
flutter run
```

### 4.2 Сценарій тестування

1. **Логін:**
   - Username: `admin`
   - Password: `admin`

2. **PIN (якщо налаштовано):**
   - Введіть PIN з Odoo або будь-який 4-значний

3. **Сканування накладної:**
   - Введіть назву накладної з Odoo (наприклад, `OUT/00001`)

4. **Сканування товарів:**
   - Вводьте баркоди товарів з накладної
   - Перевірте оновлення лічильників

5. **Підтвердження:**
   - Підтвердіть замовлення
   - Перевірте в Odoo, що picking перейшов в статус "Done"

## Крок 5: Налаштування для Production

### 5.1 Backend

**Безпека:**

```bash
# Генерація SECRET_KEY
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Додайте в `.env`:

```env
SECRET_KEY=<generated-secret-key>
DEBUG=False
```

**CORS - обмежте домени:**

В `app/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Конкретні домени
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

**HTTPS:**

```bash
# Через Nginx + Let's Encrypt
sudo apt install nginx certbot python3-certbot-nginx
sudo certbot --nginx -d api.yourdomain.com
```

### 5.2 Flutter

**Налаштування build:**

```bash
# Android
flutter build apk --release

# Підписання APK
keytool -genkey -v -keystore ~/warehouse-key.jks -keyalg RSA -keysize 2048 -validity 10000 -alias warehouse
```

В `android/app/build.gradle` додайте конфігурацію підписання.

## Troubleshooting

### Помилка: Connection refused

**Причина:** Backend не запущений або неправильна IP адреса

**Рішення:**
```bash
# Перевірте backend
curl http://localhost:8000/api/health

# Перевірте IP
ip addr show
```

### Помилка: 401 Unauthorized

**Причина:** Токен застарів або невірний

**Рішення:** Перелогіньтесь в додатку

### Помилка: Order not found

**Причина:** Накладна не існує в Odoo

**Рішення:** Створіть тестові накладні в Odoo через Sale → Orders

### Flutter не бачить backend на емуляторі

**Рішення:** Використовуйте `10.0.2.2` замість `localhost`:

```dart
static const String baseUrl = 'http://10.0.2.2:8000/api';
```

## Додаткові можливості

### Барcode Scanner камерою

Додайте `mobile_scanner` package:

```yaml
dependencies:
  mobile_scanner: ^3.5.0
```

### Offline режим

Використовуйте `sqflite` для локальної бази даних:

```yaml
dependencies:
  sqflite: ^2.3.0
```

### Push notifications

Додайте Firebase Cloud Messaging для повідомлень про нові замовлення.

## Підтримка

Для питань та підтримки звертайтесь до команди розробки.

---

**Версія:** 1.0
**Дата:** 2025-10-22
**Статус:** Готово до інтеграції
