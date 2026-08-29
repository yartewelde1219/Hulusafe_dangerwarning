import 'package:flutter/material.dart';
import 'package:url_launcher/url_launcher.dart';

import '../models/danger_event.dart';
import '../utils/formatters.dart';
import '../widgets/danger_card.dart';

class DangerDetailsScreen extends StatelessWidget {
  const DangerDetailsScreen({super.key, required this.event});

  final DangerEvent event;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Danger details')),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          Text(event.dangerType.toUpperCase(), style: Theme.of(context).textTheme.headlineSmall),
          Text('${event.dangerLevel.toUpperCase()} · Confidence ${formatPercent(event.confidence)}'),
          const SizedBox(height: 12),
          _row('Danger location', event.location.name),
          _row('Region', event.location.region),
          _row('Distance from selected location', event.distanceKm == null ? null : '${event.distanceKm!.round()} km'),
          _row('Status', event.status),
          _row('News published', formatDateTime(event.publishedAt)),
          _row('Event time', formatDateTime(event.eventTime)),
          _row('Last update', formatDateTime(event.updatedAt)),
          _row('Deaths', unknownIfNull(event.deaths)),
          _row('Injuries', unknownIfNull(event.injuries)),
          _row('Displaced', unknownIfNull(event.displaced)),
          _row('Missing', unknownIfNull(event.missing)),
          _row('Damage', unknownIfNull(event.damage)),
          _row('Trend', unknownIfNull(event.trend)),
          const SizedBox(height: 16),
          VerificationBanner(sourceCount: event.sources.length),
          const SizedBox(height: 16),
          Text('Reference sources', style: Theme.of(context).textTheme.titleMedium),
          if (event.sources.isEmpty)
            const Text('Unknown')
          else
            ...event.sources.map(
              (source) => ListTile(
                contentPadding: EdgeInsets.zero,
                title: Text(source.name),
                subtitle: Text(
                  [
                    if (source.title != null) source.title!,
                    'Published: ${formatDateTime(source.publishedAt)}',
                    if (source.credibilityScore != null)
                      'Credibility: ${formatPercent(source.credibilityScore)}',
                  ].join('\n'),
                ),
                onTap: source.url == null
                    ? null
                    : () => launchUrl(Uri.parse(source.url!), mode: LaunchMode.externalApplication),
              ),
            ),
        ],
      ),
    );
  }

  Widget _row(String label, String? value) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 4),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          SizedBox(width: 160, child: Text(label, style: const TextStyle(fontWeight: FontWeight.w600))),
          Expanded(child: Text(value ?? 'Unknown')),
        ],
      ),
    );
  }
}
