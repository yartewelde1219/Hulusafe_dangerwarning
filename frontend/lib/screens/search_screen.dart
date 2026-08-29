import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../models/danger_event.dart';
import '../providers/app_providers.dart';
import '../widgets/danger_card.dart';
import '../widgets/status_views.dart';
import 'danger_details_screen.dart';

class SearchScreen extends ConsumerStatefulWidget {
  const SearchScreen({
    super.key,
    this.initialLat,
    this.initialLon,
    this.initialQuery,
  });

  final double? initialLat;
  final double? initialLon;
  final String? initialQuery;

  @override
  ConsumerState<SearchScreen> createState() => _SearchScreenState();
}

class _SearchScreenState extends ConsumerState<SearchScreen> {
  late final TextEditingController _query;
  List<DangerEvent>? _results;
  String? _error;
  bool _loading = false;

  @override
  void initState() {
    super.initState();
    _query = TextEditingController(text: widget.initialQuery ?? '');
    if (widget.initialLat != null && widget.initialLon != null) {
      Future.microtask(_runSearch);
    }
  }

  @override
  void dispose() {
    _query.dispose();
    super.dispose();
  }

  Future<void> _runSearch() async {
    final location = ref.read(locationProvider);
    final lat = widget.initialLat ?? location.latitude;
    final lon = widget.initialLon ?? location.longitude;
    if (lat == null || lon == null) {
      setState(() => _error = 'Select a map location or grant location permission first.');
      return;
    }
    setState(() {
      _loading = true;
      _error = null;
    });
    try {
      final events = await ref.read(apiServiceProvider).search(
            lat: lat,
            lon: lon,
            query: _query.text,
          );
      setState(() => _results = events);
    } catch (error) {
      setState(() => _error = error.toString());
    } finally {
      setState(() => _loading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Search danger')),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            TextField(
              controller: _query,
              decoration: const InputDecoration(
                labelText: 'Region, zone, woreda, city, or danger type',
              ),
              onSubmitted: (_) => _runSearch(),
            ),
            const SizedBox(height: 12),
            FilledButton(onPressed: _runSearch, child: const Text('Search within 100 km')),
            const SizedBox(height: 16),
            if (_loading) const Expanded(child: LoadingState()),
            if (_error != null) Expanded(child: ErrorState(message: _error!, onRetry: _runSearch)),
            if (!_loading && _error == null && _results != null)
              Expanded(
                child: _results!.isEmpty
                    ? const EmptyState(message: 'No matching danger events.')
                    : ListView(
                        children: _results!
                            .map(
                              (event) => DangerCard(
                                event: event,
                                onTap: () => Navigator.of(context).push(
                                  MaterialPageRoute(
                                    builder: (_) => DangerDetailsScreen(event: event),
                                  ),
                                ),
                              ),
                            )
                            .toList(),
                      ),
              ),
          ],
        ),
      ),
    );
  }
}
