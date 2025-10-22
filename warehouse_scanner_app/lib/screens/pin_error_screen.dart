import 'package:flutter/material.dart';
import '../theme/app_theme.dart';

class PinErrorScreen extends StatefulWidget {
  const PinErrorScreen({super.key});

  @override
  State<PinErrorScreen> createState() => _PinErrorScreenState();
}

class _PinErrorScreenState extends State<PinErrorScreen> {
  @override
  void initState() {
    super.initState();
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
              'ПІН КОД НЕ ВІРНИЙ',
              style: TextStyle(
                fontSize: 80,
                fontWeight: FontWeight.w700,
                color: AppTheme.whitePrimary,
                height: 1.2,
              ),
              textAlign: TextAlign.center,
            ),
          ),
        ),
      ),
    );
  }
}
