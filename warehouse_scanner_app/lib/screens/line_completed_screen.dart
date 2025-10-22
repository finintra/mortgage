import 'package:flutter/material.dart';
import '../theme/app_theme.dart';

class LineCompletedScreen extends StatefulWidget {
  const LineCompletedScreen({super.key});

  @override
  State<LineCompletedScreen> createState() => _LineCompletedScreenState();
}

class _LineCompletedScreenState extends State<LineCompletedScreen> {
  @override
  void initState() {
    super.initState();
    Future.delayed(const Duration(milliseconds: 500), () {
      if (mounted) Navigator.pop(context);
    });
  }

  @override
  Widget build(BuildContext context) {
    return const Scaffold(
      backgroundColor: AppTheme.greenSuccess,
      body: Center(
        child: Text(
          'ГОТОВО.\nДАЛІ',
          style: TextStyle(fontSize: 85, fontWeight: FontWeight.w700, color: Colors.white, height: 1.3),
          textAlign: TextAlign.center,
        ),
      ),
    );
  }
}
