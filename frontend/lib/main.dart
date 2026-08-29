import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import 'providers/app_providers.dart';
import 'screens/login_screen.dart';
import 'screens/shell_screen.dart';
import 'theme/app_theme.dart';
import 'utils/constants.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  runApp(const ProviderScope(child: HuluSafeApp()));
}

class HuluSafeApp extends ConsumerWidget {
  const HuluSafeApp({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final auth = ref.watch(authProvider);
    return MaterialApp(
      title: AppConstants.appName,
      theme: buildHuluSafeTheme(),
      home: auth.isAuthenticated ? const ShellScreen() : const LoginScreen(),
    );
  }
}
