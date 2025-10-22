import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../theme/app_theme.dart';
import '../providers/app_state.dart';

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final _usernameController = TextEditingController();
  final _passwordController = TextEditingController();
  bool _isLoading = false;

  @override
  void dispose() {
    _usernameController.dispose();
    _passwordController.dispose();
    super.dispose();
  }

  Future<void> _handleLogin() async {
    if (_isLoading) return;

    setState(() => _isLoading = true);

    final appState = context.read<AppState>();
    final success = await appState.login(
      _usernameController.text,
      _passwordController.text,
    );

    setState(() => _isLoading = false);

    if (!mounted) return;

    if (success) {
      // Перехід на екран PIN
      Navigator.pushReplacementNamed(context, '/pin');
    } else {
      // Перехід на екран помилки
      Navigator.pushNamed(context, '/login-error');
    }
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
              // Заголовок
              const Text(
                'ВХІД',
                style: TextStyle(
                  fontSize: 100,
                  fontWeight: FontWeight.w700,
                ),
                textAlign: TextAlign.center,
              ),

              const SizedBox(height: 10),

              // Підзаголовок
              const Text(
                'Введіть логін та пароль',
                style: TextStyle(
                  fontSize: 28,
                  color: AppTheme.greyText,
                ),
                textAlign: TextAlign.center,
              ),

              const SizedBox(height: 40),

              // Форма
              SizedBox(
                width: double.infinity,
                child: Column(
                  children: [
                    // Поле логіна
                    SizedBox(
                      height: 60,
                      child: TextField(
                        controller: _usernameController,
                        autofocus: true,
                        textAlign: TextAlign.center,
                        style: const TextStyle(
                          fontSize: 30,
                          fontWeight: FontWeight.w500,
                        ),
                        decoration: const InputDecoration(
                          hintText: 'Логін',
                        ),
                        onSubmitted: (_) {
                          // Focus на пароль
                          FocusScope.of(context).nextFocus();
                        },
                      ),
                    ),

                    const SizedBox(height: 15),

                    // Поле пароля
                    SizedBox(
                      height: 60,
                      child: TextField(
                        controller: _passwordController,
                        obscureText: true,
                        textAlign: TextAlign.center,
                        style: const TextStyle(
                          fontSize: 30,
                          fontWeight: FontWeight.w500,
                        ),
                        decoration: const InputDecoration(
                          hintText: 'Пароль',
                        ),
                        onSubmitted: (_) => _handleLogin(),
                      ),
                    ),

                    const SizedBox(height: 25),

                    // Кнопка входу
                    SizedBox(
                      height: 70,
                      width: double.infinity,
                      child: ElevatedButton(
                        onPressed: _isLoading ? null : _handleLogin,
                        child: _isLoading
                            ? const CircularProgressIndicator(color: Colors.white)
                            : const Text(
                                'УВІЙТИ',
                                style: TextStyle(fontSize: 40),
                              ),
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
