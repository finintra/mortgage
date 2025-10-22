import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../theme/app_theme.dart';
import '../providers/app_state.dart';

class CancelPickingScreen extends StatelessWidget {
  const CancelPickingScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(20),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const Text('⚠️', style: TextStyle(fontSize: 110, color: AppTheme.redError)),
              const SizedBox(height: 20),
              const Text(
                'ВІДМІНИТИ ЗБІРКУ?',
                style: TextStyle(fontSize: 105, fontWeight: FontWeight.w700, color: AppTheme.redError),
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: 10),
              const Text(
                'Прогрес буде втрачено',
                style: TextStyle(fontSize: 32, color: AppTheme.greyText),
              ),
              const SizedBox(height: 40),
              SizedBox(
                width: double.infinity,
                height: 75,
                child: ElevatedButton(
                  onPressed: () async {
                    final appState = context.read<AppState>();
                    await appState.cancelPicking();
                    if (context.mounted) {
                      Navigator.pushNamedAndRemoveUntil(context, '/invoice-scan', (route) => false);
                    }
                  },
                  style: ElevatedButton.styleFrom(backgroundColor: AppTheme.redError),
                  child: const Text('ТАК, ВІДМІНИТИ', style: TextStyle(fontSize: 42)),
                ),
              ),
              const SizedBox(height: 15),
              SizedBox(
                width: double.infinity,
                height: 75,
                child: ElevatedButton(
                  onPressed: () => Navigator.pop(context),
                  style: ElevatedButton.styleFrom(backgroundColor: AppTheme.greyText),
                  child: const Text('НІ, ПРОДОВЖИТИ', style: TextStyle(fontSize: 42)),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
