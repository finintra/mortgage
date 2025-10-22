import 'package:flutter/foundation.dart';
import 'package:shared_preferences.dart';

class AppState extends ChangeNotifier {
  String _currentUser = '';
  String _currentOrder = '';
  int _scannedCount = 0;
  int _totalCount = 0;
  int _remainingCount = 0;
  List<String> _scannedItems = [];

  // Getters
  String get currentUser => _currentUser;
  String get currentOrder => _currentOrder;
  int get scannedCount => _scannedCount;
  int get totalCount => _totalCount;
  int get remainingCount => _remainingCount;
  List<String> get scannedItems => _scannedItems;

  // Авторизація
  Future<bool> login(String username, String password) async {
    // TODO: Реальна авторизація через API
    // Поки що просто перевіряємо, що поля не пусті
    if (username.isNotEmpty && password.isNotEmpty) {
      _currentUser = username;

      // Зберігаємо в SharedPreferences
      final prefs = await SharedPreferences.getInstance();
      await prefs.setString('current_user', username);

      notifyListeners();
      return true;
    }
    return false;
  }

  // Перевірка PIN
  Future<bool> verifyPin(String pin) async {
    // TODO: Реальна перевірка PIN через API
    // Поки що приймаємо будь-який 4-значний PIN
    return pin.length == 4;
  }

  // Скан накладної
  void scanInvoice(String invoiceNumber) {
    _currentOrder = invoiceNumber;
    // TODO: Завантажити список товарів для цієї накладної
    // Поки що ставимо тестові дані
    _totalCount = 5;
    _scannedCount = 0;
    _remainingCount = 5;
    _scannedItems = [];
    notifyListeners();
  }

  // Скан товару
  bool scanProduct(String productCode) {
    // TODO: Перевірка товару через API
    // Поки що просто додаємо до списку
    if (_remainingCount > 0) {
      _scannedItems.add(productCode);
      _scannedCount++;
      _remainingCount--;
      notifyListeners();
      return true;
    }
    return false;
  }

  // Перевірка чи товар правильний
  bool isProductValid(String productCode) {
    // TODO: Перевірка через API
    return true; // Поки що завжди true
  }

  // Перевірка чи товар зайвий
  bool isProductExtra(String productCode) {
    // TODO: Перевірка через API
    return false; // Поки що завжди false
  }

  // Підтвердження замовлення
  Future<void> confirmOrder() async {
    // TODO: Відправка підтвердження на сервер
    // Очистка даних
    _currentOrder = '';
    _scannedCount = 0;
    _totalCount = 0;
    _remainingCount = 0;
    _scannedItems = [];
    notifyListeners();
  }

  // Відміна збірки
  Future<void> cancelPicking() async {
    // TODO: Відправка відміни на сервер
    // Очистка даних
    _currentOrder = '';
    _scannedCount = 0;
    _totalCount = 0;
    _remainingCount = 0;
    _scannedItems = [];
    notifyListeners();
  }

  // Вихід з акаунту
  Future<void> logout() async {
    _currentUser = '';
    _currentOrder = '';
    _scannedCount = 0;
    _totalCount = 0;
    _remainingCount = 0;
    _scannedItems = [];

    final prefs = await SharedPreferences.getInstance();
    await prefs.remove('current_user');

    notifyListeners();
  }
}
