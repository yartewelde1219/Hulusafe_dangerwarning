import 'package:flutter/material.dart';

import '../models/danger_event.dart';
import '../utils/formatters.dart';

class DangerCard extends StatelessWidget {
  const DangerCard({super.key, required this.event, this.onTap});

  final DangerEvent event;
  final VoidCallback? onTap;

  @override
  Widget build(BuildContext context) {
    return Card(
      child: ListTile(
        onTap: onTap,
        title: Text('${event.dangerType.toUpperCase()} · ${event.dangerLevel.toUpperCase()}'),
        subtitle: Text(
          [
            event.location.name,
            if (event.distanceKm != null) '${event.distanceKm!.round()} km away',
            'News published: ${formatDateTime(event.publishedAt)}',
            'Event time: ${formatDateTime(event.eventTime)}',
            'Confidence: ${formatPercent(event.confidence)}',
          ].join('\n'),
        ),
        isThreeLine: true,
      ),
    );
  }
}

class VerificationBanner extends StatelessWidget {
  const VerificationBanner({super.key, required this.sourceCount});

  final int sourceCount;

  @override
  Widget build(BuildContext context) {
    return Card(
      color: Theme.of(context).colorScheme.secondaryContainer,
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Text(
          'This warning is based on reports from $sourceCount source(s). '
          'Review the referenced reports and other reliable information before '
          'making important decisions. HuluSafe is not an official emergency authority.',
        ),
      ),
    );
  }
}
