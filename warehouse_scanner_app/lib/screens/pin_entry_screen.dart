import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../theme/app_theme.dart';
import '../providers/app_state.dart';

class PinEntryScreen extends StatefulWidget {
  const PinEntryScreen({super.key});

  @override
  State<PinEntryScreen> createState() => _PinEntryScreenState();
}

class _PinEntryScreenState extends State<PinEntryScreen> {
  String _pin = '';
  bool _isLoading = false;

  void _addDigit(String digit) {
    if (_pin.length < 4) {
      setState(() {
        _pin += digit;
      });

      // Автоматична перевірка при 4 цифрах
      if (_pin.length == 4) {
        _verifyPin();
      }
    }
  }

  void _deleteDigit() {
    if (_pin.isNotEmpty) {
      setState(() {
        _pin = _pin.substring(0, _pin.length - 1);
      });
    }
  }

  Future<void> _verifyPin() async {
    setState(() => _isLoading = true);

    final appState = context.read<AppState>();
    final success = await appState.verifyPin(_pin);

    setState(() => _isLoading = false);

    if (!mounted) return;

    if (success) {
      // Перехід на екран сканування накладної
      Navigator.pushReplacementNamed(context, '/invoice-scan');
    } else {
      // Показати помилку і очистити PIN
      Navigator.pushNamed(context, '/pin-error');
      setState(() => _pin = '');
    }
  }

  Future<void> _handleExit() async {
    final appState = context.read<AppState>();
    await appState.logout();
    if (!mounted) return;
    Navigator.pushReplacementNamed(context, '/login');
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(20),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              // Заголовок
              const Text(
                'ВВЕДІТЬ PIN',
                style: TextStyle(
                  fontSize: 120,
                  fontWeight: FontWeight.w700,
                ),
                textAlign: TextAlign.center,
              ),

              const SizedBox(height: 40),

              // PIN індикатори
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: List.generate(4, (index) {
                  return Container(
                    width: 60,
                    height: 60,
                    margin: const EdgeInsets.symmetric(horizontal: 10),
                    decoration: BoxDecoration(
                      shape: BoxShape.circle,
                      border: Border.all(
                        color: AppTheme.blackPrimary,
                        width: 4,
                      ),
                      color: index < _pin.length
                          ? AppTheme.blackPrimary
                          : AppTheme.whitePrimary,
                    ),
                  );
                }),
              ),

              const SizedBox(height: 40),

              // Клавіатура
              SizedBox(
                width: 400,
                child: Column(
                  children: [
                    // Ряди цифр
                    for (int row = 0; row < 3; row++)
                      Padding(
                        padding: const EdgeInsets.only(bottom: 15),
                        child: Row(
                          mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                          children: [
                            for (int col = 1; col <= 3; col++)
                              _buildKey('${row * 3 + col}'),
                          ],
                        ),
                      ),

                    // Останній ряд з 0 посередині
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                      children: [
                        const SizedBox(width: 100, height: 80), // Порожнє місце
                        _buildKey('0'),
                        const SizedBox(width: 100, height: 80), // Порожнє місце
                      ],
                    ),

                    const SizedBox(height: 15),

                    // Кнопка Видалити
                    _buildDeleteKey(),

                    const SizedBox(height: 15),

                    // Кнопка Вихід
                    _buildExitKey(),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildKey(String digit) {
    return SizedBox(
      width: 100,
      height: 80,
      child: ElevatedButton(
        onPressed: _isLoading ? null : () => _addDigit(digit),
        style: ElevatedButton.styleFrom(
          backgroundColor: AppTheme.whitePrimary,
          foregroundColor: AppTheme.blackPrimary,
          side: const BorderSide(
            color: AppTheme.blackPrimary,
            width: 2,
          ),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(8),
          ),
        ),
        child: Text(
          digit,
          style: const TextStyle(
            fontSize: 50,
            fontWeight: FontWeight.w600,
          ),
        ),
      ),
    );
  }

  Widget _buildDeleteKey() {
    return SizedBox(
      width: double.infinity,
      height: 80,
      child: ElevatedButton(
        onPressed: _isLoading ? null : _deleteDigit,
        style: ElevatedButton.styleFrom(
          backgroundColor: AppTheme.greyLight,
          foregroundColor: AppTheme.blackPrimary,
          side: const BorderSide(
            color: AppTheme.blackPrimary,
            width: 2,
          ),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(8),
          ),
        ),
        child: const Text(
          'Видалити',
          style: TextStyle(
            fontSize: 40,
            fontWeight: FontWeight.w600,
          ),
        ),
      ),
    );
  }

  Widget _buildExitKey() {
    return SizedBox(
      width: double.infinity,
      height: 70,
      child: ElevatedButton(
        onPressed: _isLoading ? null : _handleExit,
        style: ElevatedButton.styleFrom(
          backgroundColor: AppTheme.whitePrimary,
          foregroundColor: AppTheme.redError,
          side: const BorderSide(
            color: AppTheme.redError,
            width: 3,
          ),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(8),
          ),
        ),
        child: const Text(
          'ВИХІД',
          style: TextStyle(
            fontSize: 36,
            fontWeight: FontWeight.w700,
          ),
        ),
      ),
    );
  }
}
