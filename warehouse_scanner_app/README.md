# Warehouse Scanner App

Додаток для сканування товарів на складі. Розроблено на Flutter для Android пристроїв.

## Опис

Це мобільний додаток для збірки замовлень на складі. Працівники можуть сканувати накладні та товари, відстежувати прогрес збірки та підтверджувати готові замовлення.

## Екрани

1. **Екран входу** - Авторизація за логіном та паролем
2. **Екран помилки входу** - Повідомлення про некоректні дані
3. **Екран PIN-коду** - Введення 4-значного PIN-коду
4. **Екран помилки PIN** - Повідомлення про некоректний PIN
5. **Екран сканування накладної** - Сканування номера накладної (OUT/...)
6. **Екран сканування товару** - Основний екран роботи з лічильниками
7. **Екран успіху** - Зелена галочка при правильному скані
8. **Екран зайвого товару** - Червоне попередження про зайвий товар
9. **Екран товару не в замовленні** - Червоний хрестик
10. **Екран завершення позиції** - "ГОТОВО. ДАЛІ"
11. **Екран завершення замовлення** - Зелений екран з результатами
12. **Екран підтвердження** - Підтвердити або відмінити замовлення
13. **Екран відміни збірки** - Попередження про втрату прогресу
14. **Екран заблокованого акаунта** - Повідомлення про деактивацію

## Вимоги

- Flutter SDK >= 3.0.0
- Dart SDK >= 3.0.0
- Android Studio або VS Code з Flutter плагіном
- Android пристрій або емулятор (мінімальна версія Android API 21)

## Встановлення

1. Клонуйте репозиторій та перейдіть в папку проекту:
```bash
cd warehouse_scanner_app
```

2. Встановіть залежності:
```bash
flutter pub get
```

3. Запустіть додаток:
```bash
flutter run
```

## Залежності

- `provider: ^6.1.1` - Управління станом додатку
- `shared_preferences: ^2.2.2` - Локальне збереження даних

## Структура проекту

```
lib/
├── main.dart                   # Точка входу, конфігурація навігації
├── theme/
│   └── app_theme.dart         # Кольори, шрифти, теми
├── providers/
│   └── app_state.dart         # Глобальний стан додатку
├── widgets/
│   └── scan_input_zone.dart   # Віджет для сканування з кнопкою камери
└── screens/
    ├── login_screen.dart
    ├── login_error_screen.dart
    ├── pin_entry_screen.dart
    ├── pin_error_screen.dart
    ├── invoice_scan_screen.dart
    ├── product_scan_screen.dart
    ├── success_screen.dart
    ├── error_extra_screen.dart
    ├── error_not_in_order_screen.dart
    ├── line_completed_screen.dart
    ├── order_completed_screen.dart
    ├── confirm_order_screen.dart
    ├── cancel_picking_screen.dart
    └── account_locked_screen.dart
```

## Особливості

- **Портретна орієнтація** - Додаток працює тільки в портретному режимі
- **Повноекранний режим** - Приховані системні кнопки для зручності
- **Великі шрифти** - Розміри оптимізовані для швидкого читання
- **Високий контраст** - Кольори підібрані для роботи в складських умовах
- **Автофокус** - Автоматичне фокусування на полях вводу
- **Підтримка апаратного сканера** - Працює як звичайна клавіатура

## Налаштування цільового розміру екрану

Додаток оптимізований для стандартних Android пристроїв з роздільною здатністю 360x740px.

## Інтеграція з бекендом

У файлі `lib/providers/app_state.dart` позначені місця, де потрібно додати API виклики:

- `login()` - Авторизація користувача
- `verifyPin()` - Перевірка PIN-коду
- `scanInvoice()` - Завантаження даних накладної
- `scanProduct()` - Перевірка товару
- `confirmOrder()` - Підтвердження замовлення
- `cancelPicking()` - Відміна збірки

Приклад інтеграції:
```dart
Future<bool> login(String username, String password) async {
  final response = await http.post(
    Uri.parse('$API_URL/auth/login'),
    body: {'username': username, 'password': password},
  );

  if (response.statusCode == 200) {
    _currentUser = username;
    notifyListeners();
    return true;
  }
  return false;
}
```

## Додавання сканування штрих-кодів камерою

Рекомендована бібліотека: `mobile_scanner`

1. Додайте в `pubspec.yaml`:
```yaml
dependencies:
  mobile_scanner: ^3.5.0
```

2. Додайте права в `android/app/src/main/AndroidManifest.xml`:
```xml
<uses-permission android:name="android.permission.CAMERA" />
<uses-feature android:name="android.hardware.camera" />
```

3. Реалізуйте в `scan_input_zone.dart`:
```dart
void _openScanner(BuildContext context) async {
  final result = await Navigator.push(
    context,
    MaterialPageRoute(builder: (context) => const BarcodeScannerScreen()),
  );
  if (result != null) {
    controller.text = result;
    onSubmitted(result);
  }
}
```

## Тестування

Запустіть тести:
```bash
flutter test
```

## Збірка APK

Для розробки:
```bash
flutter build apk --debug
```

Для релізу:
```bash
flutter build apk --release
```

APK файл буде в `build/app/outputs/flutter-apk/`

## Збірка AAB (для Google Play)

```bash
flutter build appbundle --release
```

## Колірна схема

- Зелений успіх: `#4CAF50`
- Червона помилка: `#F44336`
- Помаранчеве попередження: `#FF9800`
- Сірий текст: `#757575`
- Чорний основний: `#000000`

## Ліцензія

Цей проект розроблений для внутрішнього використання.

## Підтримка

Для питань та підтримки звертайтесь до команди розробки.
