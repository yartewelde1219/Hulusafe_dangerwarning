import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../providers/app_providers.dart';
import '../utils/formatters.dart';
import '../widgets/danger_card.dart';
import '../widgets/status_views.dart';
import 'danger_details_screen.dart';

class DashboardScreen extends ConsumerWidget {
  const DashboardScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final location = ref.watch(locationProvider);
    final dashboard = ref.watch(dashboardProvider);

    if (!location.permissionGranted) {
      return ErrorState(
        message: location.error ??
            'HuluSafe needs location permission to show nearby danger information.',
        onRetry: () => ref.read(locationProvider.notifier).requestAndLoad(),
      );
    }

    return dashboard.when(
      loading: () => const LoadingState(message: 'Loading nearby danger…'),
      error: (error, _) => ErrorState(
        message: error.toString(),
        onRetry: () => ref.invalidate(dashboardProvider),
      ),
      data: (data) {
        final highest = data.highestNearbyDanger;
        return RefreshIndicator(
          onRefresh: () async => ref.invalidate(dashboardProvider),
          child: ListView(
            padding: const EdgeInsets.all(16),
            children: [
              Text('Current area', style: Theme.of(context).textTheme.titleMedium),
              Text(data.areaName, style: Theme.of(context).textTheme.headlineSmall),
              const SizedBox(height: 16),
              if (highest == null)
                const EmptyState(message: 'No active nearby danger within 100 km.')
              else ...[
                Text('Highest nearby danger', style: Theme.of(context).textTheme.titleMedium),
                DangerCard(
                  event: highest,
                  onTap: () => Navigator.of(context).push(
                    MaterialPageRoute(builder: (_) => DangerDetailsScreen(event: highest)),
                  ),
                ),
                Text('Last update: ${formatDateTime(highest.updatedAt ?? highest.publishedAt)}'),
              ],
              const SizedBox(height: 24),
              Text('Recent alerts', style: Theme.of(context).textTheme.titleMedium),
              if (data.recentAlerts.isEmpty)
                const EmptyState(message: 'No recent alerts.')
              else
                ...data.recentAlerts.map(
                  (event) => DangerCard(
                    event: event,
                    onTap: () => Navigator.of(context).push(
                      MaterialPageRoute(builder: (_) => DangerDetailsScreen(event: event)),
                    ),
                  ),
                ),
            ],
          ),
        );
      },
    );
  }
}
