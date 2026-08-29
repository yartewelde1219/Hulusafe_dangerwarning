import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../models/dashboard.dart';
import '../models/danger_event.dart';
import '../services/api_service.dart';
import '../services/auth_service.dart';
import '../services/location_service.dart';

final apiServiceProvider = Provider<ApiService>((ref) => ApiService());
final authServiceProvider = Provider<AuthService>((ref) => AuthService());
final locationServiceProvider = Provider<LocationService>((ref) => LocationService());

class AuthState {
  const AuthState({this.user, this.error});

  final AuthUser? user;
  final String? error;

  bool get isAuthenticated => user != null;
}

class AuthNotifier extends StateNotifier<AuthState> {
  AuthNotifier(this._authService) : super(const AuthState());

  final AuthService _authService;

  Future<void> signIn(String email, String password) async {
    try {
      final user = await _authService.signIn(email: email, password: password);
      state = AuthState(user: user);
    } catch (error) {
      state = AuthState(error: error.toString());
    }
  }

  Future<void> signOut() async {
    await _authService.signOut();
    state = const AuthState();
  }
}

final authProvider = StateNotifierProvider<AuthNotifier, AuthState>((ref) {
  return AuthNotifier(ref.watch(authServiceProvider));
});

class LocationState {
  const LocationState({
    this.latitude,
    this.longitude,
    this.permissionGranted = false,
    this.error,
  });

  final double? latitude;
  final double? longitude;
  final bool permissionGranted;
  final String? error;
}

class LocationNotifier extends StateNotifier<LocationState> {
  LocationNotifier(this._locationService) : super(const LocationState());

  final LocationService _locationService;

  Future<void> requestAndLoad() async {
    final granted = await _locationService.ensurePermission();
    if (!granted) {
      state = const LocationState(
        permissionGranted: false,
        error: 'Location permission is required for nearby danger information.',
      );
      return;
    }
    final coords = await _locationService.currentCoordinates();
    state = LocationState(
      permissionGranted: true,
      latitude: coords.latitude,
      longitude: coords.longitude,
    );
  }
}

final locationProvider = StateNotifierProvider<LocationNotifier, LocationState>((ref) {
  return LocationNotifier(ref.watch(locationServiceProvider));
});

final dashboardProvider = FutureProvider<DashboardData>((ref) async {
  final location = ref.watch(locationProvider);
  if (!location.permissionGranted || location.latitude == null || location.longitude == null) {
    throw Exception('Location permission is required to load the dashboard.');
  }
  return ref.watch(apiServiceProvider).fetchDashboard(
        lat: location.latitude!,
        lon: location.longitude!,
      );
});

final regionalDangerProvider = FutureProvider<List<RegionalDanger>>((ref) {
  return ref.watch(apiServiceProvider).fetchRegionalDanger();
});

final alertHistoryProvider = FutureProvider<List<DangerEvent>>((ref) {
  return ref.watch(apiServiceProvider).fetchAlertHistory();
});
