import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:hulusafe/main.dart';

void main() {
  testWidgets('shows sign-in for unauthenticated users', (tester) async {
    await tester.pumpWidget(const ProviderScope(child: HuluSafeApp()));
    expect(find.text('HuluSafe'), findsOneWidget);
    expect(find.text('Sign in'), findsOneWidget);
  });
}
