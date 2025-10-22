import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../theme/app_theme.dart';
import '../providers/app_state.dart';
import '../widgets/scan_input_zone.dart';

class InvoiceScanScreen extends StatefulWidget {
  const InvoiceScanScreen({super.key});

  @override
  State<InvoiceScanScreen> createState() => _InvoiceScanScreenState();
}

class _InvoiceScanScreenState extends State<InvoiceScanScreen> {
  final _controller = TextEditingController();

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  void _handleScan(String value) {
    if (value.isEmpty) return;

    final appState = context.read<AppState>();
    appState.scanInvoice(value);

    Navigator.pushReplacementNamed(context, '/product-scan');
  }

  void _handleCamera() {
    // TODO: Відкрити камеру для скану
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Камера'),
        content: const Text('Камера відкриється для сканування накладної'),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('OK'),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(20),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const Text(
                'СКАНУЙ НАКЛАДНУ',
                style: TextStyle(
                  fontSize: 80,
                  fontWeight: FontWeight.w700,
                ),
                textAlign: TextAlign.center,
              ),

              const SizedBox(height: 15),

              const Text(
                '📄',
                style: TextStyle(fontSize: 80),
              ),

              const SizedBox(height: 15),

              const Text(
                'Піднесіть сканер до накладної OUT/...',
                style: TextStyle(
                  fontSize: 28,
                  color: AppTheme.greyText,
                ),
                textAlign: TextAlign.center,
              ),

              const SizedBox(height: 30),

              ScanInputZone(
                controller: _controller,
                placeholder: 'OUT/...',
                onCameraPressed: _handleCamera,
                onSubmitted: _handleScan,
                hint: 'Або натисніть камеру для сканування',
              ),
            ],
          ),
        ),
      ),
    );
  }
}
