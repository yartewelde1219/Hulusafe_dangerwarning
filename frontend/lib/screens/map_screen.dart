import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:google_maps_flutter/google_maps_flutter.dart';

import '../models/dashboard.dart';
import '../providers/app_providers.dart';
import '../widgets/status_views.dart';
import 'search_screen.dart';

class MapScreen extends ConsumerWidget {
  const MapScreen({super.key});

  static const _ethiopia = CameraPosition(
    target: LatLng(9.145, 40.4897),
    zoom: 5.4,
  );

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

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final regions = ref.watch(regionalDangerProvider);
    return regions.when(
      loading: () => const LoadingState(message: 'Loading Ethiopia danger map…'),
      error: (error, _) => ErrorState(
        message: error.toString(),
        onRetry: () => ref.invalidate(regionalDangerProvider),
      ),
      data: (items) {
        final markers = <Marker>{};
        for (final region in items) {
          if (region.latitude == null || region.longitude == null) continue;
          markers.add(
            Marker(
              markerId: MarkerId(region.regionName),
              position: LatLng(region.latitude!, region.longitude!),
              infoWindow: InfoWindow(
                title: region.regionName,
                snippet: '${region.dangerType} · ${region.level} · ${(region.confidence * 100).round()}%',
              ),
              icon: BitmapDescriptor.defaultMarkerWithHue(
                HSVColor.fromColor(_levelColor(region.level)).hue,
              ),
              onTap: () => Navigator.of(context).push(
                MaterialPageRoute(
                  builder: (_) => SearchScreen(
                    initialLat: region.latitude,
                    initialLon: region.longitude,
                    initialQuery: region.regionName,
                  ),
                ),
              ),
            ),
          );
        }
        return Column(
          children: [
            Padding(
              padding: const EdgeInsets.all(8),
              child: Wrap(
                spacing: 8,
                children: const [
                  Chip(label: Text('No active danger'), avatar: CircleAvatar(backgroundColor: Colors.green)),
                  Chip(label: Text('Low'), avatar: CircleAvatar(backgroundColor: Colors.yellow)),
                  Chip(label: Text('Moderate'), avatar: CircleAvatar(backgroundColor: Colors.orange)),
                  Chip(label: Text('High'), avatar: CircleAvatar(backgroundColor: Colors.red)),
                  Chip(label: Text('Critical'), avatar: CircleAvatar(backgroundColor: Colors.purple)),
                ],
              ),
            ),
            Expanded(
              child: GoogleMap(
                initialCameraPosition: _ethiopia,
                markers: markers,
                myLocationEnabled: true,
                myLocationButtonEnabled: true,
                onTap: (latLng) => Navigator.of(context).push(
                  MaterialPageRoute(
                    builder: (_) => SearchScreen(
                      initialLat: latLng.latitude,
                      initialLon: latLng.longitude,
                    ),
                  ),
                ),
              ),
            ),
            const Padding(
              padding: EdgeInsets.all(8),
              child: Text('Tap the map or a region marker to inspect danger within 100 km.'),
            ),
          ],
        );
      },
    );
  }
}
