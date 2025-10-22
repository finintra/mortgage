import 'package:flutter/material.dart';
import '../theme/app_theme.dart';

class ErrorNotInOrderScreen extends StatefulWidget {
  const ErrorNotInOrderScreen({super.key});

  @override
  State<ErrorNotInOrderScreen> createState() => _ErrorNotInOrderScreenState();
}

class _ErrorNotInOrderScreenState extends State<ErrorNotInOrderScreen> {
  @override
  void initState() {
    super.initState();
    Future.delayed(const Duration(milliseconds: 800), () {
      if (mounted) Navigator.pop(context);
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppTheme.redError,
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: const [
            Text('✕', style: TextStyle(fontSize: 130, color: Colors.white)),
            SizedBox(height: 10),
            Text(
              'ЦЬОГО ТОВАРУ\nНЕМАЄ У\nЗАМОВЛЕННІ',
              style: TextStyle(fontSize: 65, fontWeight: FontWeight.w700, color: Colors.white, height: 1.2),
              textAlign: TextAlign.center,
            ),
          ],
        ),
      ),
    );
  }
}
