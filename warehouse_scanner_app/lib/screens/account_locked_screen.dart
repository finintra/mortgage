import 'package:flutter/material.dart';
import '../theme/app_theme.dart';

class AccountLockedScreen extends StatelessWidget {
  const AccountLockedScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return const Scaffold(
      body: SafeArea(
        child: Center(
          child: Padding(
            padding: EdgeInsets.all(20),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Text('🔒', style: TextStyle(fontSize: 100)),
                SizedBox(height: 20),
                Text(
                  'АКАУНТ\nДЕАКТИВОВАНО',
                  style: TextStyle(fontSize: 70, fontWeight: FontWeight.w700),
                  textAlign: TextAlign.center,
                ),
                SizedBox(height: 20),
                Text(
                  'Зверніться до адміністратора',
                  style: TextStyle(fontSize: 30, color: AppTheme.greyText),
                  textAlign: TextAlign.center,
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
