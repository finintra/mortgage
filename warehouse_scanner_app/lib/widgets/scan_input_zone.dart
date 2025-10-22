import 'package:flutter/material.dart';
import '../theme/app_theme.dart';

class ScanInputZone extends StatelessWidget {
  final TextEditingController controller;
  final String placeholder;
  final VoidCallback onCameraPressed;
  final Function(String) onSubmitted;
  final String? hint;

  const ScanInputZone({
    super.key,
    required this.controller,
    required this.placeholder,
    required this.onCameraPressed,
    required this.onSubmitted,
    this.hint,
  });

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Row(
          children: [
            // Поле вводу
            Expanded(
              child: SizedBox(
                height: 60,
                child: TextField(
                  controller: controller,
                  autofocus: true,
                  textAlign: TextAlign.center,
                  style: const TextStyle(
                    fontSize: 30,
                    fontWeight: FontWeight.w500,
                  ),
                  decoration: InputDecoration(
                    hintText: placeholder,
                    hintStyle: TextStyle(
                      color: AppTheme.greyText.withOpacity(0.6),
                    ),
                  ),
                  onSubmitted: onSubmitted,
                ),
              ),
            ),

            const SizedBox(width: 10),

            // Кнопка камери
            Container(
              width: 60,
              height: 60,
              decoration: BoxDecoration(
                color: AppTheme.greyLight,
                border: Border.all(
                  color: AppTheme.blackPrimary,
                  width: 3,
                ),
                borderRadius: BorderRadius.circular(10),
              ),
              child: IconButton(
                onPressed: onCameraPressed,
                icon: const Icon(Icons.camera_alt, size: 35),
                padding: EdgeInsets.zero,
              ),
            ),
          ],
        ),

        // Підказка
        if (hint != null) ...[
          const SizedBox(height: 10),
          Text(
            hint!,
            style: const TextStyle(
              fontSize: 20,
              color: AppTheme.greyText,
            ),
            textAlign: TextAlign.center,
          ),
        ],
      ],
    );
  }
}
