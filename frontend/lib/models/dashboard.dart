import 'danger_event.dart';

class DashboardData {
  const DashboardData({
    required this.areaName,
    this.highestNearbyDanger,
    this.nearbyDangers = const [],
    this.recentAlerts = const [],
  });

  final String areaName;
  final DangerEvent? highestNearbyDanger;
  final List<DangerEvent> nearbyDangers;
  final List<DangerEvent> recentAlerts;

  factory DashboardData.fromJson(Map<String, dynamic> json) {
    List<DangerEvent> parseEvents(String key) {
      final items = json[key] as List<dynamic>? ?? [];
      return items
          .whereType<Map<String, dynamic>>()
          .map(DangerEvent.fromJson)
          .toList();
    }

    final highest = json['highest_nearby_danger'] as Map<String, dynamic>?;
    return DashboardData(
      areaName: json['area_name'] as String? ?? 'Unknown area',
      highestNearbyDanger: highest == null ? null : DangerEvent.fromJson(highest),
      nearbyDangers: parseEvents('nearby_dangers'),
      recentAlerts: parseEvents('recent_alerts'),
    );
  }
}

class RegionalDanger {
  const RegionalDanger({
    required this.regionName,
    required this.dangerType,
    required this.level,
    required this.confidence,
    this.latitude,
    this.longitude,
  });

  final String regionName;
  final String dangerType;
  final String level;
  final double confidence;
  final double? latitude;
  final double? longitude;

  factory RegionalDanger.fromJson(Map<String, dynamic> json) {
    return RegionalDanger(
      regionName: json['region_name'] as String? ?? 'Unknown',
      dangerType: json['danger_type'] as String? ?? 'none',
      level: json['level'] as String? ?? 'none',
      confidence: (json['confidence'] as num?)?.toDouble() ?? 0,
      latitude: (json['latitude'] as num?)?.toDouble(),
      longitude: (json['longitude'] as num?)?.toDouble(),
    );
  }
}
