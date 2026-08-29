import 'package:intl/intl.dart';

String formatDateTime(DateTime? value) {
  if (value == null) return 'Unknown';
  return DateFormat('d MMM yyyy, HH:mm').format(value.toLocal());
}

String formatPercent(double? value) {
  if (value == null) return 'Unknown';
  return '${(value * 100).round()}%';
}

String unknownIfNull(Object? value) {
  if (value == null) return 'Unknown';
  if (value is String && value.trim().isEmpty) return 'Unknown';
  return value.toString();
}
