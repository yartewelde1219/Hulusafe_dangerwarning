import 'package:flutter/material.dart';
import 'package:flutter_map/flutter_map.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:latlong2/latlong.dart';

import '../providers/app_providers.dart';
import '../widgets/status_views.dart';
import 'search_screen.dart';

class MapScreen extends ConsumerWidget {
  const MapScreen({super.key});

  static const _ethiopia = LatLng(9.145, 40.4897);

  Color _levelColor(String level) {
    switch (level.toLowerCase()) {
      case 'low':
        return Colors.yellow.shade700;
      case 'moderate':
        return Colors.orange;
      case 'high':
        return Colors.red;
      case 'critical':
        return Colors.purple;
      default:
        return Colors.green;
    }
  }

  Marker _marker({
    required LatLng point,
    required String label,
    required String level,
    required VoidCallback onTap,
  }) {
    return Marker(
      point: point,
      width: 150,
      height: 64,
      child: GestureDetector(
        onTap: onTap,
        child: Column(
          children: [
            Icon(Icons.location_on, color: _levelColor(level), size: 34),
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 5, vertical: 2),
              color: Colors.white.withValues(alpha: 0.9),
              child: Text(
                label,
                maxLines: 1,
                overflow: TextOverflow.ellipsis,
                style: const TextStyle(fontSize: 11, fontWeight: FontWeight.w600),
              ),
            ),
          ],
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final regions = ref.watch(regionalDangerProvider);
    final dashboard = ref.watch(dashboardProvider);
    return regions.when(
      loading: () => const LoadingState(message: 'Loading Ethiopia danger map...'),
      error: (error, _) => ErrorState(
        message: error.toString(),
        onRetry: () => ref.invalidate(regionalDangerProvider),
      ),
      data: (items) {
        final markers = <Marker>[];
        for (final region in items) {
          if (region.latitude == null || region.longitude == null) continue;
          markers.add(_marker(
            point: LatLng(region.latitude!, region.longitude!),
            label: region.regionName,
            level: region.level,
            onTap: () => Navigator.of(context).push(
              MaterialPageRoute(
                builder: (_) => SearchScreen(
                  initialLat: region.latitude,
                  initialLon: region.longitude,
                  initialQuery: region.regionName,
                ),
              ),
            ),
          ));
        }
        dashboard.whenData((data) {
          for (final event in data.nearbyDangers) {
            final location = event.location;
            if (location.latitude == null || location.longitude == null) continue;
            markers.add(_marker(
              point: LatLng(location.latitude!, location.longitude!),
              label: '${event.dangerType}: ${location.name}',
              level: event.dangerLevel,
              onTap: () => Navigator.of(context).push(
                MaterialPageRoute(
                  builder: (_) => SearchScreen(
                    initialLat: location.latitude,
                    initialLon: location.longitude,
                    initialQuery: location.name,
                  ),
                ),
              ),
            ));
          }
        });

        final location = ref.read(locationProvider);
        final center = location.latitude != null && location.longitude != null
            ? LatLng(location.latitude!, location.longitude!)
            : _ethiopia;
        if (location.latitude != null && location.longitude != null) {
          markers.add(
            Marker(
              point: LatLng(location.latitude!, location.longitude!),
              width: 42,
              height: 42,
              child: const Icon(Icons.person_pin_circle, color: Colors.blue, size: 36),
            ),
          );
        }

        return Column(
          children: [
            const Padding(
              padding: EdgeInsets.fromLTRB(8, 8, 8, 0),
              child: Wrap(
                spacing: 8,
                children: [
                  Chip(label: Text('None'), avatar: CircleAvatar(backgroundColor: Colors.green)),
                  Chip(label: Text('Low'), avatar: CircleAvatar(backgroundColor: Color(0xFFC9A227))),
                  Chip(label: Text('Moderate'), avatar: CircleAvatar(backgroundColor: Colors.orange)),
                  Chip(label: Text('High'), avatar: CircleAvatar(backgroundColor: Colors.red)),
                  Chip(label: Text('Critical'), avatar: CircleAvatar(backgroundColor: Colors.purple)),
                ],
              ),
            ),
            Expanded(
              child: FlutterMap(
                options: MapOptions(
                  initialCenter: center,
                  initialZoom: location.latitude == null ? 5.4 : 8,
                  onTap: (_, point) => Navigator.of(context).push(
                    MaterialPageRoute(
                      builder: (_) => SearchScreen(
                        initialLat: point.latitude,
                        initialLon: point.longitude,
                      ),
                    ),
                  ),
                ),
                children: [
                  TileLayer(
                    urlTemplate: 'https://tile.openstreetmap.org/{z}/{x}/{y}.png',
                    userAgentPackageName: 'com.hulusafe.hulusafe',
                  ),
                  MarkerLayer(markers: markers),
                  const RichAttributionWidget(
                    attributions: [
                      TextSourceAttribution('OpenStreetMap contributors'),
                    ],
                  ),
                ],
              ),
            ),
            const Padding(
              padding: EdgeInsets.all(8),
              child: Text('Tap the map or a marker to inspect danger within 100 km.'),
            ),
          ],
        );
      },
    );
  }
}
