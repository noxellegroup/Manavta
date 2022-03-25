import 'package:flutter/material.dart';
import 'package:flutter_signin_button/flutter_signin_button.dart';
import 'secret_keys.dart' as SecretKey;
import 'dart:async';
import 'package:uni_links/uni_links.dart';
import 'package:url_launcher/url_launcher.dart';
import 'auth_service.dart';


final AuthService authService = AuthService();

class LoginScreen extends StatefulWidget {
  const LoginScreen({Key? key}) : super(key: key);

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {

  StreamSubscription? subs;
  bool loader =false;
  @override
  void initState() {
    loader = false;
    _initDeepLinkListener();
    super.initState();
  }
  @override
  void dispose() {
    _disposeDeepLinkListener();
    super.dispose();
  }
  void _initDeepLinkListener() async {
    subs = getLinksStream().listen((String? link) {
      if(link!=null){_checkDeepLink(link);}

    }, cancelOnError: true);
  }
  void _checkDeepLink(String link) {
    if (link != null) {
      String code = link.substring(link.indexOf(RegExp('code=')) + 5);
      authService.loginWithGitHub(code)
          .then((firebaseUser) {
        print(firebaseUser.email);
        print(firebaseUser.photoURL);
        if (firebaseUser.displayName == null) {
          print("Name Not found");
        }
        else{
          print("LOGGED IN AS: " + firebaseUser.displayName!);
        }

      }).catchError((e) {
        print("LOGIN ERROR: " + e.toString());
      });
    }
  }

  void _disposeDeepLinkListener() {
    if (subs != null) {
      subs!.cancel();
      subs = null;
    }
  }


  void onClickGitHubLoginButton() async {
    const String url = "https://github.com/login/oauth/authorize" +
        "?client_id=" + SecretKey.GITHUB_CLIENT_ID +
        "&scope=public_repo%20read:user%20user:email";

    if (await canLaunch(url)) {
      setState(() {
        loader = true;
      });
      await launch(
        url,
        forceSafariVC: false,
        forceWebView: false,
      );
    } else {
      setState(() {
        loader = false;
      });
      print("CANNOT LAUNCH THIS URL!");
    }
  }
  
  @override
  Widget build(BuildContext context) {
    return Scaffold(
        backgroundColor: Color.fromRGBO(42, 43, 56 ,100),
        body: ListView(
          children: <Widget>[
            Stack(
              children: <Widget>[
                Container(
                  height: 220,
                  decoration: new BoxDecoration(
                    image: new DecorationImage(
                      image: new AssetImage('assets/chatbot.jpg'),

                      fit: BoxFit.cover,
                    ),
                  ),
                ),
                Padding(
                    padding: EdgeInsets.only(top: 185),
                    child: Center(
                      child: Card(
                        color: Color.fromRGBO(82, 104, 143,10),
                        child: Padding(
                          padding: EdgeInsets.only(
                              top: 4, bottom: 4, left: 4, right: 4),
                          child: Container(
                            height: 50,
                            width: 220,
                            child: Center(child: Text('Manavta',
                              style: TextStyle(fontFamily: 'Hubballi',fontSize: 50,color: Colors.amberAccent[100]),)),
                          ),


                        ),
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(8.0),
                        ),
                        elevation: 5,
                      ),
                    )),
              ],
            ),


            Container(

              margin: EdgeInsets.only(top:MediaQuery.of(context).size.height*0.2),
padding: EdgeInsets.all(20),

                child: SignInButton(

                  Buttons.GitHub,
                  text: "Sign in with Twitter",
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(30)),
                  onPressed: () async {
                     onClickGitHubLoginButton();



                  },
                )),

            SizedBox(height: 80),
          ],
        ));
  }
}
