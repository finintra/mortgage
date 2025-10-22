import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../theme/app_theme.dart';
import '../providers/app_state.dart';

class ConfirmOrderScreen extends StatelessWidget {
  const ConfirmOrderScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(20),
          child: Consumer<AppState>(
            builder: (context, appState, _) {
              return Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  SizedBox(
                    width: double.infinity,
                    height: 120,
                    child: ElevatedButton(
                      onPressed: () async {
                        await appState.confirmOrder();
                        if (context.mounted) {
                          Navigator.pushNamedAndRemoveUntil(context, '/invoice-scan', (route) => false);
                        }
                      },
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          const Text('ЗАТВЕРДИТИ ЦЕ ЗАМОВЛЕННЯ', style: TextStyle(fontSize: 48)),
                          const SizedBox(height: 5),
                          Text('(${appState.currentOrder})', style: const TextStyle(fontSize: 42)),
                        ],
                      ),
                    ),
                  ),
                  const SizedBox(height: 40),
                  SizedBox(
                    width: double.infinity,
                    height: 80,
                    child: OutlinedButton(
                      onPressed: () {
                        Navigator.pushNamed(context, '/cancel-picking');
                      },
                      style: OutlinedButton.styleFrom(
                        foregroundColor: AppTheme.orangeWarning,
                        side: const BorderSide(color: AppTheme.orangeWarning, width: 3),
                        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                      ),
                      child: const Text('ВІДМІНИ ЗАМОВЛЕННЯ', style: TextStyle(fontSize: 42, fontWeight: FontWeight.w600)),
                    ),
                  ),
                  const SizedBox(height: 20),
                  Text(
                    'Натисніть для підтвердження',
                    style: TextStyle(fontSize: 30, color: AppTheme.greyText.withOpacity(0.5)),
                  ),
                ],
              );
            },
          ),
        ),
      ),
    );
  }
}
