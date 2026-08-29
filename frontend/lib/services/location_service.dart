import 'package:geolocator/geolocator.dart';

class UserCoordinates {
  const UserCoordinates({required this.latitude, required this.longitude});

  final double latitude;
  final double longitude;
}

class LocationService {
  Future<bool> ensurePermission() async {
    final serviceEnabled = await Geolocator.isLocationServiceEnabled();
    if (!serviceEnabled) return false;

    var permission = await Geolocator.checkPermission();
    if (permission == LocationPermission.denied) {
      permission = await Geolocator.requestPermission();
    }
    return permission == LocationPermission.always ||
        permission == LocationPermission.whileInUse;
  }

  Future<LocationPermission> currentPermission() {
    return Geolocator.checkPermission();
  }

  Future<UserCoordinates> currentCoordinates() async {
    final position = await Geolocator.getCurrentPosition(
      locationSettings: const LocationSettings(accuracy: LocationAccuracy.medium),
    );
    return UserCoordinates(
      latitude: position.latitude,
      longitude: position.longitude,
    );
  }
}
