import 'dart:convert';
import 'package:http/http.dart' as http;
import 'secret_keys.dart' as SecretKey;

import 'package:firebase_auth/firebase_auth.dart' as auth;
import 'github_login_request.dart';
import 'github_login_response.dart';

class AuthService{

  final auth.FirebaseAuth _firebaseAuth = auth.FirebaseAuth.instance;

  Future<auth.User> loginWithGitHub(String code) async {
    //ACCESS TOKEN REQUEST
    final response = await http.post(
      Uri.parse( "https://github.com/login/oauth/access_token"),

      headers: {
        "Content-Type": "application/json",
        "Accept": "application/json"
      },
      body: jsonEncode(GitHubLoginRequest(
        clientId: SecretKey.GITHUB_CLIENT_ID,
        clientSecret: SecretKey.GITHUB_CLIENT_SECRET,
        code: code,
      )),
    );

    GitHubLoginResponse loginResponse = GitHubLoginResponse.fromJson(json.decode(response.body));

    //FIREBASE SIGNIN
    final auth.AuthCredential credential = auth.GithubAuthProvider.credential(loginResponse.accessToken);

    final auth.User user = (await _firebaseAuth.signInWithCredential(credential)).user!;
    return user;
  }

  void signOutWithGitHub() async {
    _firebaseAuth.signOut();
  }
}