class AppConstants {
  static const String appName = 'HuluSafe';
  static const double defaultAlertRadiusKm = 100;
  static const int maxAlertEventAgeDays = 14;
  static const String apiBaseUrl = String.fromEnvironment(
    'API_BASE_URL',
    defaultValue: 'http://127.0.0.1:8000',
  );

  static const String safetyDisclaimer =
      'HuluSafe is an information and warning-support system, not an official '
      'emergency authority. Always review referenced media before acting.';
}
