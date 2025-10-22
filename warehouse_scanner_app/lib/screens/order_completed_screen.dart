import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../theme/app_theme.dart';
import '../providers/app_state.dart';

class OrderCompletedScreen extends StatelessWidget {
  const OrderCompletedScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppTheme.greenSuccess,
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(20),
          child: Consumer<AppState>(
            builder: (context, appState, _) {
              return Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  const Text(
                    'ЗАМОВЛЕННЯ\nЗІБРАНО',
                    style: TextStyle(fontSize: 65, fontWeight: FontWeight.w700, color: Colors.white),
                    textAlign: TextAlign.center,
                  ),
                  const SizedBox(height: 20),
                  Text(
                    '${appState.totalCount} ШТУК',
                    style: const TextStyle(fontSize: 85, fontWeight: FontWeight.w700, color: Colors.white),
                  ),
                  const SizedBox(height: 30),
                  const Text(
                    'НАКЛЕЙТЕ ТТН\nТА НАТИСНІТЬ',
                    style: TextStyle(fontSize: 50, fontWeight: FontWeight.w600, color: Colors.white),
                    textAlign: TextAlign.center,
                  ),
                  const SizedBox(height: 30),
                  SizedBox(
                    width: double.infinity,
                    height: 70,
                    child: ElevatedButton(
                      onPressed: () {
                        Navigator.pushReplacementNamed(context, '/confirm-order');
                      },
                      style: ElevatedButton.styleFrom(
                        backgroundColor: Colors.white,
                        foregroundColor: AppTheme.greenSuccess,
                      ),
                      child: const Text('ПІДТВЕРДИТИ', style: TextStyle(fontSize: 45)),
                    ),
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
