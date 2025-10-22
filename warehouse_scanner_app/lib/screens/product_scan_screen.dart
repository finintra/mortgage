import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../theme/app_theme.dart';
import '../providers/app_state.dart';
import '../widgets/scan_input_zone.dart';

class ProductScanScreen extends StatefulWidget {
  const ProductScanScreen({super.key});

  @override
  State<ProductScanScreen> createState() => _ProductScanScreenState();
}

class _ProductScanScreenState extends State<ProductScanScreen> {
  final _controller = TextEditingController();

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  void _handleScan(String value) {
    if (value.isEmpty) return;

    final appState = context.read<AppState>();
    
    // Перевірка валідності товару
    if (!appState.isProductValid(value)) {
      Navigator.pushNamed(context, '/error-not-in-order');
      _controller.clear();
      return;
    }

    if (appState.isProductExtra(value)) {
      Navigator.pushNamed(context, '/error-extra');
      _controller.clear();
      return;
    }

    // Успішне сканування
    appState.scanProduct(value);
    Navigator.pushNamed(context, '/success');
    _controller.clear();

    // Перевірка чи всі товари відскануванні
    if (appState.remainingCount == 0) {
      Future.delayed(const Duration(milliseconds: 500), () {
        if (mounted) {
          Navigator.pushReplacementNamed(context, '/order-completed');
        }
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: Consumer<AppState>(
          builder: (context, appState, _) {
            return Column(
              children: [
                // Заголовок з номером замовлення
                Container(
                  width: double.infinity,
                  padding: const EdgeInsets.all(10),
                  decoration: const BoxDecoration(
                    border: Border(
                      bottom: BorderSide(
                        color: AppTheme.blackPrimary,
                        width: 3,
                      ),
                    ),
                  ),
                  child: Text(
                    appState.currentOrder,
                    style: const TextStyle(
                      fontSize: 45,
                      fontWeight: FontWeight.w700,
                    ),
                    textAlign: TextAlign.center,
                  ),
                ),

                // Основна зона
                Expanded(
                  child: Padding(
                    padding: const EdgeInsets.symmetric(horizontal: 15, vertical: 10),
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        const Text(
                          'СКАНУЙ: SKU-12345',
                          style: TextStyle(
                            fontSize: 35,
                            fontWeight: FontWeight.w600,
                          ),
                        ),

                        const SizedBox(height: 5),

                        const Text(
                          'Назва товару приклад',
                          style: TextStyle(
                            fontSize: 22,
                            color: AppTheme.greyText,
                          ),
                        ),

                        const SizedBox(height: 15),

                        // Лічильники
                        Column(
                          children: [
                            // ЗАЛИШОК
                            Container(
                              width: double.infinity,
                              padding: const EdgeInsets.all(12),
                              decoration: BoxDecoration(
                                color: AppTheme.orangeLight,
                                borderRadius: BorderRadius.circular(12),
                              ),
                              child: Column(
                                children: [
                                  const Text(
                                    'ЗАЛИШОК',
                                    style: TextStyle(
                                      fontSize: 22,
                                      fontWeight: FontWeight.w500,
                                      color: AppTheme.orangeWarning,
                                    ),
                                  ),
                                  Text(
                                    '${appState.remainingCount}',
                                    style: const TextStyle(
                                      fontSize: 100,
                                      fontWeight: FontWeight.w700,
                                      color: AppTheme.orangeWarning,
                                      height: 1,
                                    ),
                                  ),
                                ],
                              ),
                            ),

                            const SizedBox(height: 8),

                            // ВЖЕ
                            Container(
                              width: double.infinity,
                              padding: const EdgeInsets.all(12),
                              decoration: BoxDecoration(
                                color: AppTheme.greenLight,
                                borderRadius: BorderRadius.circular(12),
                              ),
                              child: Column(
                                children: [
                                  const Text(
                                    'ВЖЕ',
                                    style: TextStyle(
                                      fontSize: 22,
                                      fontWeight: FontWeight.w500,
                                      color: AppTheme.greenSuccess,
                                    ),
                                  ),
                                  Text(
                                    '${appState.scannedCount}',
                                    style: const TextStyle(
                                      fontSize: 100,
                                      fontWeight: FontWeight.w700,
                                      color: AppTheme.greenSuccess,
                                      height: 1,
                                    ),
                                  ),
                                ],
                              ),
                            ),
                          ],
                        ),

                        const SizedBox(height: 15),

                        // Зона сканування
                        ScanInputZone(
                          controller: _controller,
                          placeholder: 'Скануйте товар',
                          onCameraPressed: () {},
                          onSubmitted: _handleScan,
                          hint: 'Або натисніть камеру',
                        ),

                        const SizedBox(height: 10),

                        const Text(
                          'Тільки скан товару або ВІДМІНА ЗБІРКИ',
                          style: TextStyle(
                            fontSize: 20,
                            color: AppTheme.greyText,
                          ),
                          textAlign: TextAlign.center,
                        ),
                      ],
                    ),
                  ),
                ),

                // Кнопка відміни
                Container(
                  padding: const EdgeInsets.all(15),
                  decoration: const BoxDecoration(
                    border: Border(
                      top: BorderSide(
                        color: Color(0xFFE0E0E0),
                        width: 2,
                      ),
                    ),
                  ),
                  child: SizedBox(
                    width: double.infinity,
                    height: 55,
                    child: ElevatedButton(
                      onPressed: () {
                        Navigator.pushNamed(context, '/cancel-picking');
                      },
                      style: ElevatedButton.styleFrom(
                        backgroundColor: AppTheme.orangeWarning,
                      ),
                      child: const Text(
                        'ВІДМІНИТИ ЗБІРКУ',
                        style: TextStyle(fontSize: 28),
                      ),
                    ),
                  ),
                ),
              ],
            );
          },
        ),
      ),
    );
  }
}
