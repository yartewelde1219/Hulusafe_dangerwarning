class AuthUser {
  const AuthUser({required this.id, required this.email, this.displayName});

  final String id;
  final String email;
  final String? displayName;
}

/// Placeholder auth until Firebase Authentication is wired by Students 1 and 3.
class AuthService {
  AuthUser? _currentUser;

  AuthUser? get currentUser => _currentUser;

  Future<AuthUser> signIn({required String email, required String password}) async {
    if (email.isEmpty || password.length < 6) {
      throw Exception('Enter a valid email and a password with at least 6 characters.');
    }
    _currentUser = AuthUser(id: email, email: email, displayName: email.split('@').first);
    return _currentUser!;
  }

  Future<AuthUser> signUp({required String email, required String password}) {
    return signIn(email: email, password: password);
  }

  Future<void> signOut() async {
    _currentUser = null;
  }
}
