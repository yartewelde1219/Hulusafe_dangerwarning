import 'dart:convert';

import 'package:http/http.dart' as http;

import '../models/danger_event.dart';
import '../models/dashboard.dart';
import '../utils/constants.dart';

class ApiService {
  ApiService({http.Client? client}) : _client = client ?? http.Client();

  final http.Client _client;
  String? _authToken;

  void setAuthToken(String? token) => _authToken = token;

  Map<String, String> get _headers => {
        'Accept': 'application/json',
        if (_authToken != null) 'Authorization': 'Bearer $_authToken',
      };

  Uri _uri(String path, [Map<String, String>? query]) {
    return Uri.parse('${AppConstants.apiBaseUrl}$path').replace(queryParameters: query);
  }

  Future<DashboardData> fetchDashboard({
    required double lat,
    required double lon,
  }) async {
    final response = await _client.get(
      _uri('/dashboard', {
        'lat': lat.toString(),
        'lon': lon.toString(),
      }),
      headers: _headers,
    );
    return DashboardData.fromJson(_decode(response));
  }

  Future<List<RegionalDanger>> fetchRegionalDanger() async {
    final response = await _client.get(_uri('/regions/danger'), headers: _headers);
    final payload = _decode(response);
    final items = payload['regions'] as List<dynamic>? ?? [];
    return items
        .whereType<Map<String, dynamic>>()
        .map(RegionalDanger.fromJson)
        .toList();
  }

  Future<List<DangerEvent>> search({
    required double lat,
    required double lon,
    String? query,
    String? dangerType,
  }) async {
    final response = await _client.get(
      _uri('/search', {
        'lat': lat.toString(),
        'lon': lon.toString(),
        'radius_km': AppConstants.defaultAlertRadiusKm.toString(),
        if (query != null && query.isNotEmpty) 'q': query,
        if (dangerType != null && dangerType.isNotEmpty) 'danger_type': dangerType,
      }),
      headers: _headers,
    );
    final payload = _decode(response);
    final items = payload['events'] as List<dynamic>? ?? [];
    return items.whereType<Map<String, dynamic>>().map(DangerEvent.fromJson).toList();
  }

  Future<List<DangerEvent>> nearbyDangers({
    required double lat,
    required double lon,
  }) async {
    final response = await _client.get(
      _uri('/nearby-dangers', {
        'lat': lat.toString(),
        'lon': lon.toString(),
        'radius_km': AppConstants.defaultAlertRadiusKm.toString(),
      }),
      headers: _headers,
    );
    final payload = _decode(response);
    final items = payload['events'] as List<dynamic>? ?? [];
    return items.whereType<Map<String, dynamic>>().map(DangerEvent.fromJson).toList();
  }

  Future<DangerEvent> fetchEvent(String eventId) async {
    final response = await _client.get(_uri('/events/$eventId'), headers: _headers);
    return DangerEvent.fromJson(_decode(response));
  }

  Future<List<DangerEvent>> fetchAlertHistory() async {
    final response = await _client.get(_uri('/alerts/history'), headers: _headers);
    final payload = _decode(response);
    final items = payload['alerts'] as List<dynamic>? ?? [];
    return items.whereType<Map<String, dynamic>>().map(DangerEvent.fromJson).toList();
  }

  Map<String, dynamic> _decode(http.Response response) {
    if (response.statusCode < 200 || response.statusCode >= 300) {
      throw Exception('API error ${response.statusCode}: ${response.body}');
    }
    return jsonDecode(response.body) as Map<String, dynamic>;
  }
}
