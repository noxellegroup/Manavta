import 'package:bubble/bubble.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
//import 'package:flutter_dialogflow/dialogflow_v2.dart';
import 'package:intl/intl.dart';
import 'package:font_awesome_flutter/font_awesome_flutter.dart';
import 'package:flutter_svg_provider/flutter_svg_provider.dart';
import 'auth_service.dart';
import 'loginscreen.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:firebase_auth/firebase_auth.dart';
var route = '/auth';
final AuthService authService = AuthService();
Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Firebase.initializeApp();
  runApp(MyApp());
}

class MyApp extends StatelessWidget {

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Manavta',
      theme: ThemeData.dark(),
      debugShowCheckedModeBanner: false,
      home: LandingPage(),
      //home: MyHomePage(title: 'Manavta'),
    );
  }
}

class LandingPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return StreamBuilder<User?>(
      stream: FirebaseAuth.instance.authStateChanges(),
      builder: (context, snapshot) {
        if (snapshot.connectionState == ConnectionState.active) {

          User? user = snapshot.data;

          if (user == null) {
            return const LoginScreen();
          }
          return MyHomePage(user:user,title: 'Manavta');
        } else {
          return const Scaffold(
            body: Center(
              child: CircularProgressIndicator(),
            ),
          );
        }
      },
    );
  }
}




class MyHomePage extends StatefulWidget {
  final User user;
  MyHomePage({ required this.user ,required this.title}) ;

  final String title;
  @override
  _MyHomePageState createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  // void response(query) async {
  //   AuthGoogle authGoogle = await AuthGoogle(
  //       fileJson: "assets/service.json")
  //       .build();
  //   Dialogflow dialogflow =
  //   Dialogflow(authGoogle: authGoogle, language: Language.english);
  //   AIResponse aiResponse = await dialogflow.detectIntent(query);
  //   setState(() {
  //     messsages.insert(0, {
  //       "data": 0,
  //       "message": aiResponse.getListMessage()[0]["text"]["text"][0].toString()
  //     });
  //   });
  //
  //
  //   print(aiResponse.getListMessage()[0]["text"]["text"][0].toString());
  // }


  final messageInsert = TextEditingController();
  List<Map> messsages = [];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Colors.transparent,
        centerTitle: true,
        title: Container(
          child: Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
            CircleAvatar(
              backgroundImage: AssetImage("assets/robot.jpg"),
            ),
            SizedBox(
              width: MediaQuery.of(context).size.width*0.02 ,
            ),
            Text(
              "Manavta",
            ),

          ],),
        ),
        // Text(
        //   "Manavta",
        // ),
      ),
      body: Container(


        decoration: BoxDecoration(
            image: DecorationImage(image: Svg(
              'assets/pat.svg',
            ),
            fit: BoxFit.cover,
          ),
         color: Color.fromRGBO(42, 43, 56 ,100),
        ),

        child: Column(
          children: <Widget>[
            Container(
              padding: EdgeInsets.only(top: 15, bottom: 10),
              child: Text("Today, ${DateFormat("jm").format(DateTime.now())}", style: TextStyle(
                  fontSize: 20
              ),),
            ),
            Flexible(
                child: ListView.builder(
                    reverse: true,
                    itemCount: messsages.length,
                    itemBuilder: (context, index) => chat(
                        messsages[index]["message"].toString(),
                        messsages[index]["data"]))),
            // SizedBox(
            //   height: 20,
            // ),

            // Divider(
            //   height: 5.0,
            //   color: Colors.blue,
            // ),
            Container(

              decoration: BoxDecoration(
                  borderRadius: BorderRadius.circular(50),
                  boxShadow: [
                    BoxShadow(
                      color: Color(0xFF000000).withAlpha(60),
                      blurRadius: 6.0,
                      spreadRadius: 0.0,
                      offset: Offset(
                        0.0,
                        0.0,
                      ),
                    ),
                  ]),


              child: ListTile(

                leading: IconButton(
                  onPressed: null,
                  icon: Icon(Icons.mic_rounded, color: Colors.amberAccent[100],
                     size: 35,),
                 // color: Color.fromRGBO(35, 39, 42,100),
                ),

                title: Container(
                  height: MediaQuery.of(context).size.height*0.05,
                  decoration: BoxDecoration(
                    borderRadius: BorderRadius.all(Radius.circular(
                        15)),
                    color: Color.fromRGBO(220, 220, 220, 100),
                  ),
                  //padding: EdgeInsets.only(left: 15),
                  child: Padding(
                    padding: const EdgeInsets.only(left: 10),
                    child: TextFormField(

                      controller: messageInsert,
                      decoration: InputDecoration(
                        // fillColor: Color.fromRGBO(44, 47, 51, 100),
                        // filled: true,
                        hintText: "Enter a Message...",
                        hintStyle: TextStyle(
                            color: Colors.black26
                        ),
                        border: InputBorder.none,
                        focusedBorder: InputBorder.none,
                        enabledBorder: InputBorder.none,
                        errorBorder: InputBorder.none,
                        disabledBorder: InputBorder.none,
                      ),

                      style: TextStyle(
                          fontSize: 16,
                          color: Colors.black
                      ),
                      onChanged: (value) {

                      },
                    ),
                  ),
                ),

                trailing: IconButton(

                    icon: Icon(

                      Icons.send,
                      size: 30.0,
                     color: Colors.amberAccent[100],
                    ),
                    onPressed: () {

                      if (messageInsert.text.isEmpty) {
                        print("empty message");
                      } else {
                        setState(() {
                          messsages.insert(0,
                              {"data": 1, "message": messageInsert.text});
                        });
                        // response(messageInsert.text);
                        messageInsert.clear();
                      }
                      FocusScopeNode currentFocus = FocusScope.of(context);
                      if (!currentFocus.hasPrimaryFocus) {
                        currentFocus.unfocus();
                      }
                    }),

              ),

            ),

            SizedBox(
              height: 15.0,
            )
          ],
        ),
      ),
    );
  }

  //for better one i have use the bubble package check out the pubspec.yaml

  Widget chat(String message, int data) {
    return Container(
      padding: EdgeInsets.only(left: 20, right: 20),

      child: Row(
        mainAxisAlignment: data == 1 ? MainAxisAlignment.end : MainAxisAlignment.start,
        children: [

          data == 0 ? Container(
            height: 60,
            width: 60,
            child: CircleAvatar(
              backgroundImage: AssetImage("assets/robot.jpg"),
            ),
          ) : Container(),

          Padding(
            padding: EdgeInsets.all(20.0),
            child: Bubble(
                radius: Radius.circular(15.0),
                color: data == 0 ? Color.fromRGBO(23, 157, 139, 1) : Color.fromRGBO(31, 32, 41, 100),
                elevation: 0.0,

                child: Padding(
                  padding: EdgeInsets.all(2.0),
                  child: Row(
                    mainAxisSize: MainAxisSize.min,
                    children: <Widget>[

                      SizedBox(
                        width: 10.0,
                      ),
                      Flexible(
                          child: Container(
                            constraints: BoxConstraints( maxWidth: 200),
                            child: Text(
                              message,
                              style: TextStyle(
                                  color: Colors.white, fontWeight: FontWeight.bold),
                            ),
                          ))
                    ],
                  ),
                )),
          ),


          data == 1? Container(
            height: 60,
            width: 60,
            child: CircleAvatar(
              radius: 20,

              backgroundImage: AssetImage("assets/default.jpg"),
            ),
          ) : Container(),

        ],
      ),
    );
  }
}