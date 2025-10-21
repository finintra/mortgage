# Статичні HTML демо екрани / Static HTML Demo Screens

Цей каталог містить повністю самодостатні HTML файли для демонстрації всіх екранів додатку.

This directory contains fully self-contained HTML files to demonstrate all app screens.

## Як переглянути / How to View

Просто відкрийте `index.html` у браузері!

Just open `index.html` in your browser!

```bash
# Відкрити в браузері / Open in browser
open demo/index.html

# Або використовуйте будь-який локальний веб-сервер
# Or use any local web server
cd demo
python3 -m http.server 8000
# Потім відкрийте / Then open: http://localhost:8000
```

## Список екранів / Screen List

### 1. Авторизація / Authentication
- `screen-01-badge-scan.html` - Скан бейджа
- `screen-01b-badge-error.html` - Помилка бейджа
- `screen-02-pin-entry.html` - Введення PIN

### 2. Прив'язка замовлення / Order Binding
- `screen-03-invoice-scan.html` - Скан накладної

### 3. Робочий процес / Working Process
- `screen-04-product-scan.html` - Сканування товарів (ГОЛОВНИЙ)
- `screen-05-success.html` - Успішний скан
- `screen-06-error-extra.html` - Помилка: Лишній товар
- `screen-07-error-not-in-order.html` - Помилка: Немає в замовленні
- `screen-08-line-completed.html` - Рядок закрито

### 4. Завершення замовлення / Order Completion
- `screen-09-order-completed.html` - Замовлення зібрано
- `screen-10-confirm-order.html` - Підтвердження замовлення

### 5. Додаткові / Additional
- `screen-11-cancel-picking.html` - Відміна збірки
- `screen-12-account-locked.html` - Акаунт заблоковано

## Особливості / Features

✅ Повністю самодостатні файли (все CSS вбудовано)
✅ Responsive дизайн (працює на будь-яких пристроях)
✅ Великі шрифти згідно специфікації (120-200px)
✅ Точні кольори (#4CAF50, #F44336, #FF9800)
✅ Навігація між екранами
✅ Можна відкрити без інтернету

---

Створено для демонстрації дизайну мобільного складського додатку.

Created to demonstrate mobile warehouse app design.
