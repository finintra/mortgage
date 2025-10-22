import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:provider/provider.dart';
import 'theme/app_theme.dart';
import 'screens/login_screen.dart';
import 'screens/login_error_screen.dart';
import 'screens/pin_entry_screen.dart';
import 'screens/pin_error_screen.dart';
import 'screens/invoice_scan_screen.dart';
import 'screens/product_scan_screen.dart';
import 'screens/success_screen.dart';
import 'screens/error_extra_screen.dart';
import 'screens/error_not_in_order_screen.dart';
import 'screens/line_completed_screen.dart';
import 'screens/order_completed_screen.dart';
import 'screens/confirm_order_screen.dart';
import 'screens/cancel_picking_screen.dart';
import 'screens/account_locked_screen.dart';
import 'providers/app_state.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();

  // Налаштування орієнтації - тільки portrait
  SystemChrome.setPreferredOrientations([
    DeviceOrientation.portraitUp,
    DeviceOrientation.portraitDown,
  ]);

  // Сховати системні кнопки для повноекранного режиму
  SystemChrome.setEnabledSystemUIMode(SystemUiMode.immersiveSticky);

  runApp(const WarehouseScannerApp());
}

class WarehouseScannerApp extends StatelessWidget {
  const WarehouseScannerApp({super.key});

  @override
  Widget build(BuildContext context) {
    return ChangeNotifierProvider(
      create: (_) => AppState(),
      child: MaterialApp(
        title: 'Warehouse Scanner',
        theme: AppTheme.theme,
        debugShowCheckedModeBanner: false,
        initialRoute: '/login',
        routes: {
          '/login': (context) => const LoginScreen(),
          '/login-error': (context) => const LoginErrorScreen(),
          '/pin': (context) => const PinEntryScreen(),
          '/pin-error': (context) => const PinErrorScreen(),
          '/invoice-scan': (context) => const InvoiceScanScreen(),
          '/product-scan': (context) => const ProductScanScreen(),
          '/success': (context) => const SuccessScreen(),
          '/error-extra': (context) => const ErrorExtraScreen(),
          '/error-not-in-order': (context) => const ErrorNotInOrderScreen(),
          '/line-completed': (context) => const LineCompletedScreen(),
          '/order-completed': (context) => const OrderCompletedScreen(),
          '/confirm-order': (context) => const ConfirmOrderScreen(),
          '/cancel-picking': (context) => const CancelPickingScreen(),
          '/account-locked': (context) => const AccountLockedScreen(),
        },
      ),
    );
  }
}
