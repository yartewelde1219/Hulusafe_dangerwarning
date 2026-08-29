class EventLocation {
  const EventLocation({
    required this.name,
    this.region,
    this.zone,
    this.woreda,
    this.latitude,
    this.longitude,
  });

  final String name;
  final String? region;
  final String? zone;
  final String? woreda;
  final double? latitude;
  final double? longitude;

  factory EventLocation.fromJson(Map<String, dynamic> json) {
    return EventLocation(
      name: json['name'] as String? ?? 'Unknown',
      region: json['region'] as String?,
      zone: json['zone'] as String?,
      woreda: json['woreda'] as String?,
      latitude: (json['latitude'] as num?)?.toDouble(),
      longitude: (json['longitude'] as num?)?.toDouble(),
    );
  }
}

class EventSource {
  const EventSource({
    required this.name,
    this.title,
    this.url,
    this.publishedAt,
    this.credibilityScore,
  });

  final String name;
  final String? title;
  final String? url;
  final DateTime? publishedAt;
  final double? credibilityScore;

  factory EventSource.fromJson(Map<String, dynamic> json) {
    return EventSource(
      name: json['name'] as String? ?? 'Unknown source',
      title: json['title'] as String?,
      url: json['url'] as String?,
      publishedAt: DateTime.tryParse(json['published_at'] as String? ?? ''),
      credibilityScore: (json['credibility_score'] as num?)?.toDouble(),
    );
  }
}

class DangerEvent {
  const DangerEvent({
    required this.eventId,
    required this.dangerType,
    required this.dangerLevel,
    required this.confidence,
    required this.location,
    required this.status,
    this.eventTime,
    this.publishedAt,
    this.updatedAt,
    this.distanceKm,
    this.deaths,
    this.injuries,
    this.displaced,
    this.missing,
    this.damage,
    this.trend,
    this.sources = const [],
  });

  final String eventId;
  final String dangerType;
  final String dangerLevel;
  final double confidence;
  final EventLocation location;
  final String status;
  final DateTime? eventTime;
  final DateTime? publishedAt;
  final DateTime? updatedAt;
  final double? distanceKm;
  final int? deaths;
  final int? injuries;
  final int? displaced;
  final int? missing;
  final String? damage;
  final String? trend;
  final List<EventSource> sources;

  factory DangerEvent.fromJson(Map<String, dynamic> json) {
    final locationJson = json['location'] as Map<String, dynamic>? ?? {};
    final sourcesJson = json['sources'] as List<dynamic>? ?? [];
    return DangerEvent(
      eventId: json['event_id'] as String? ?? '',
      dangerType: json['danger_type'] as String? ?? 'other',
      dangerLevel: json['danger_level'] as String? ?? 'unknown',
      confidence: (json['confidence'] as num?)?.toDouble() ?? 0,
      location: EventLocation.fromJson(locationJson),
      status: json['status'] as String? ?? 'unknown',
      eventTime: DateTime.tryParse(json['event_time'] as String? ?? ''),
      publishedAt: DateTime.tryParse(json['published_at'] as String? ?? ''),
      updatedAt: DateTime.tryParse(json['updated_at'] as String? ?? ''),
      distanceKm: (json['distance_km'] as num?)?.toDouble(),
      deaths: json['deaths'] as int?,
      injuries: json['injuries'] as int?,
      displaced: json['displaced'] as int?,
      missing: json['missing'] as int?,
      damage: json['damage'] as String?,
      trend: json['trend'] as String?,
      sources: sourcesJson
          .whereType<Map<String, dynamic>>()
          .map(EventSource.fromJson)
          .toList(),
    );
  }
}
