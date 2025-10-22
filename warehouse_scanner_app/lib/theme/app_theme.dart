import 'package:flutter/material.dart';

class AppTheme {
  // Кольорова палітра
  static const Color greenSuccess = Color(0xFF4CAF50);
  static const Color redError = Color(0xFFF44336);
  static const Color orangeWarning = Color(0xFFFF9800);
  static const Color greyText = Color(0xFF757575);
  static const Color blackPrimary = Color(0xFF000000);
  static const Color whitePrimary = Color(0xFFFFFFFF);

  // Background кольори для лічильників
  static const Color orangeLight = Color(0xFFFFF3E0);
  static const Color greenLight = Color(0xFFE8F5E9);
  static const Color greyLight = Color(0xFFF5F5F5);

  // Розміри екрану (цільові)
  static const double targetWidth = 360.0;
  static const double targetHeight = 740.0;

  // Базова тема
  static ThemeData get theme {
    return ThemeData(
      primaryColor: greenSuccess,
      scaffoldBackgroundColor: whitePrimary,
      fontFamily: 'Roboto',

      // Стиль кнопок
      elevatedButtonTheme: ElevatedButtonThemeData(
        style: ElevatedButton.styleFrom(
          backgroundColor: greenSuccess,
          foregroundColor: whitePrimary,
          textStyle: const TextStyle(
            fontSize: 40,
            fontWeight: FontWeight.w600,
          ),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(12),
          ),
          minimumSize: const Size(double.infinity, 70),
        ),
      ),

      // Стиль текстових полів
      inputDecorationTheme: InputDecorationTheme(
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(10),
          borderSide: const BorderSide(
            color: blackPrimary,
            width: 3,
          ),
        ),
        enabledBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(10),
          borderSide: const BorderSide(
            color: blackPrimary,
            width: 3,
          ),
        ),
        focusedBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(10),
          borderSide: const BorderSide(
            color: greenSuccess,
            width: 3,
          ),
        ),
        filled: true,
        fillColor: whitePrimary,
        contentPadding: const EdgeInsets.symmetric(
          horizontal: 20,
          vertical: 15,
        ),
      ),

      // Стилі текстів
      textTheme: const TextTheme(
        displayLarge: TextStyle(
          fontSize: 100,
          fontWeight: FontWeight.w700,
          color: blackPrimary,
        ),
        displayMedium: TextStyle(
          fontSize: 80,
          fontWeight: FontWeight.w700,
          color: blackPrimary,
        ),
        headlineLarge: TextStyle(
          fontSize: 60,
          fontWeight: FontWeight.w700,
          color: blackPrimary,
        ),
        headlineMedium: TextStyle(
          fontSize: 50,
          fontWeight: FontWeight.w700,
          color: blackPrimary,
        ),
        bodyLarge: TextStyle(
          fontSize: 32,
          fontWeight: FontWeight.w400,
          color: greyText,
        ),
        bodyMedium: TextStyle(
          fontSize: 24,
          fontWeight: FontWeight.w400,
          color: greyText,
        ),
      ),
    );
  }

  // Responsive font size helper
  static double responsiveFontSize(BuildContext context, double min, double preferred, double max) {
    final width = MediaQuery.of(context).size.width;
    final scale = width / targetWidth;
    final size = preferred * scale;
    return size.clamp(min, max);
  }
}
