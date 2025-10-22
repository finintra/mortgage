import 'package:flutter/material.dart';
import '../theme/app_theme.dart';

class ErrorExtraScreen extends StatefulWidget {
  const ErrorExtraScreen({super.key});

  @override
  State<ErrorExtraScreen> createState() => _ErrorExtraScreenState();
}

class _ErrorExtraScreenState extends State<ErrorExtraScreen> {
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
            Text('⚠', style: TextStyle(fontSize: 150, color: Colors.white)),
            SizedBox(height: 10),
            Text(
              'ЦЕ ЛИШНІЙ\nТОВАР',
              style: TextStyle(fontSize: 70, fontWeight: FontWeight.w700, color: Colors.white, height: 1.2),
              textAlign: TextAlign.center,
            ),
          ],
        ),
      ),
    );
  }
}
