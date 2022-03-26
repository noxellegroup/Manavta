// import 'package:flutter/material.dart';
// import 'package:twitter_login/twitter_login.dart';
//
//
//
// Future login() async {
//   final twitterLogin= new TwitterLogin(
//       apiKey: 'QDe6utJhJgWL5vphrQ3gTor2Z',
//       apiSecretKey: 'DdEx5Q6tmoKWpj1mjgaQRa0v3u24evXhxFFxCgw8KxIDEPDAOR',
//       redirectURI: 'https://twitter.com/login');
//
//
//   final authResult = await twitterLogin.login();
//   switch (authResult.status) {
//     case TwitterLoginStatus.loggedIn:
//     // success
//       print('====== Login success ======');
//       break;
//     case TwitterLoginStatus.cancelledByUser:
//     // cancel
//       print('====== Login cancel ======');
//       break;
//     case TwitterLoginStatus.error:
//     case null:
//     // error
//       print('====== Login error ======');
//       break;
//   }
// }
import 'package:flutter/material.dart';
// import 'package:github_sign_in/github_sign_in.dart';
//
// import 'package:github_sign_in/github_sign_in.dart';

// Future<UserCredential> signInWithGitHub() async {
//   // Create a GitHubSignIn instance
//   final GitHubSignIn gitHubSignIn = GitHubSignIn(
//       clientId: clientId,
//       clientSecret: clientSecret,
//       redirectUrl: 'https://my-project.firebaseapp.com/__/auth/handler');
//
//   // Trigger the sign-in flow
//   final result = await gitHubSignIn.signIn(context);
//
//   // Create a credential from the access token
//   final githubAuthCredential = GithubAuthProvider.credential(result.token);
//
//   // Once signed in, return the UserCredential
//   return await FirebaseAuth.instance.signInWithCredential(githubAuthCredential);
// }
