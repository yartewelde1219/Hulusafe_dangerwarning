import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:geolocator/geolocator.dart';

import '../providers/app_providers.dart';
import '../services/location_service.dart';
import '../utils/constants.dart';

class SettingsScreen extends ConsumerStatefulWidget {
  const SettingsScreen({super.key});

  @override
  ConsumerState<SettingsScreen> createState() => _SettingsScreenState();
}

class _SettingsScreenState extends ConsumerState<SettingsScreen> {
  bool _notificationsEnabled = true;
  String _permissionLabel = 'Checking…';

  @override
  void initState() {
    super.initState();
    _loadPermission();
  }

  Future<void> _loadPermission() async {
    final permission = await LocationService().currentPermission();
    setState(() {
      _permissionLabel = switch (permission) {
        LocationPermission.always || LocationPermission.whileInUse => 'Granted',
        LocationPermission.deniedForever => 'Denied permanently',
        _ => 'Denied',
      };
    });
  }

  @override
  Widget build(BuildContext context) {
    final auth = ref.watch(authProvider);
    return ListView(
      padding: const EdgeInsets.all(16),
      children: [
        SwitchListTile(
          title: const Text('Danger notifications'),
          subtitle: const Text('Personalized alerts for eligible nearby events'),
          value: _notificationsEnabled,
          onChanged: (value) => setState(() => _notificationsEnabled = value),
        ),
        ListTile(
          title: const Text('Location permission'),
          subtitle: Text(_permissionLabel),
          trailing: TextButton(
            onPressed: () async {
              await ref.read(locationProvider.notifier).requestAndLoad();
              await _loadPermission();
            },
            child: const Text('Update'),
          ),
        ),
        const ListTile(
          title: Text('Alert preferences'),
          subtitle: Text('100 km radius · 14-day event age limit'),
        ),
        const Divider(),
        ListTile(
          title: const Text('Signed in as'),
          subtitle: Text(auth.user?.email ?? 'Guest'),
        ),
        ListTile(
          title: const Text('Privacy'),
          subtitle: const Text(
            'Exact coordinates are sent only when needed for nearby danger queries. '
            'The dashboard shows an approximate area name, not a public pin of your home.',
          ),
        ),
        const ListTile(
          title: Text('About HuluSafe'),
          subtitle: Text(AppConstants.safetyDisclaimer),
        ),
        FilledButton(
          onPressed: () => ref.read(authProvider.notifier).signOut(),
          child: const Text('Sign out'),
        ),
      ],
    );
  }
}
