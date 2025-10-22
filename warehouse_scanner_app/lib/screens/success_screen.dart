import 'package:flutter/material.dart';
import '../theme/app_theme.dart';

class SuccessScreen extends StatefulWidget {
  const SuccessScreen({super.key});

  @override
  State<SuccessScreen> createState() => _SuccessScreenState();
}

class _SuccessScreenState extends State<SuccessScreen> {
  @override
  void initState() {
    super.initState();
    Future.delayed(const Duration(milliseconds: 400), () {
      if (mounted) Navigator.pop(context);
    });
  }

  @override
  Widget build(BuildContext context) {
    return const Scaffold(
      backgroundColor: AppTheme.greenSuccess,
      body: Center(
        child: Text(
          '✓',
          style: TextStyle(fontSize: 150, color: Colors.white),
        ),
      ),
    );
  }
}
