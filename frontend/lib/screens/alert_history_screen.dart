import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../providers/app_providers.dart';
import '../widgets/danger_card.dart';
import '../widgets/status_views.dart';
import 'danger_details_screen.dart';

class AlertHistoryScreen extends ConsumerWidget {
  const AlertHistoryScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final history = ref.watch(alertHistoryProvider);
    return Scaffold(
      appBar: AppBar(title: const Text('Alert history')),
      body: history.when(
        loading: () => const LoadingState(),
        error: (error, _) => ErrorState(
          message: error.toString(),
          onRetry: () => ref.invalidate(alertHistoryProvider),
        ),
        data: (alerts) {
          if (alerts.isEmpty) {
            return const EmptyState(message: 'No personalized alerts yet.');
          }
          return ListView(
            padding: const EdgeInsets.all(16),
            children: alerts
                .map(
                  (event) => DangerCard(
                    event: event,
                    onTap: () => Navigator.of(context).push(
                      MaterialPageRoute(builder: (_) => DangerDetailsScreen(event: event)),
                    ),
                  ),
                )
                .toList(),
          );
        },
      ),
    );
  }
}
