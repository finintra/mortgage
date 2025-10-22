import 'package:flutter/material.dart';
import '../theme/app_theme.dart';

class LoginErrorScreen extends StatefulWidget {
  const LoginErrorScreen({super.key});

  @override
  State<LoginErrorScreen> createState() => _LoginErrorScreenState();
}

class _LoginErrorScreenState extends State<LoginErrorScreen> {
  @override
  void initState() {
    super.initState();
    // Автоматичне повернення через 2 секунди
    Future.delayed(const Duration(seconds: 2), () {
      if (mounted) {
        Navigator.pop(context);
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppTheme.redError,
      body: SafeArea(
        child: Center(
          child: Padding(
            padding: const EdgeInsets.all(20),
            child: Text(
              'НЕКОРЕКТНИЙ ЛОГІН АБО ПАРОЛЬ.\nСПРОБУЙТЕ ЗНОВУ',
              style: TextStyle(
                fontSize: 70,
                fontWeight: FontWeight.w700,
                color: AppTheme.whitePrimary,
                height: 1.3,
              ),
              textAlign: TextAlign.center,
            ),
          ),
        ),
      ),
    );
  }
}
