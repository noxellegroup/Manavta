import 'package:avatar_glow/avatar_glow.dart';
import 'package:bubble/bubble.dart';
import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import 'package:flutter_svg_provider/flutter_svg_provider.dart';
import 'auth_service.dart';
import 'loginscreen.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:graphql_flutter/graphql_flutter.dart';
import 'package:speech_to_text/speech_to_text.dart' as stt;
var route = '/auth';
final AuthService authService = AuthService();
Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Firebase.initializeApp();

  runApp(MyApp());
}

class MyApp extends StatelessWidget {

  //const MyApp({ }) ;
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

  //speech to text

  late stt.SpeechToText _speech;
  bool _isListening = false;
  String _text = '';
  double _confidence = 1.0;
  //speech
  @override
  void initState() {

    super.initState();
    _speech=stt.SpeechToText();

  }


  void response(query) async {

    HttpLink httpLink = HttpLink(
      'https://countries.trevorblades.com/'
    );

    GraphQLClient graphql = GraphQLClient(
      link: httpLink,
      cache: GraphQLCache(),
    );

    final String whattofetch = """
    query fetchthis {
      country(code: "${query}"){
      capital
      }
    }
  """;

    QueryOptions q = QueryOptions(document: gql(whattofetch));


    var result = await graphql.query(q);
    String resultE = result.data!['country']['capital'];

    setState(() {
      messsages.insert(0, {
        "data": 0,
        "message":resultE
      });
    });
    print('hello');
   print(result.data!['country']['capital']);


  }

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

                leading: AvatarGlow(
                  animate: _isListening,
                  glowColor: Colors.amberAccent,
                  endRadius: 40,
                  duration: const Duration(milliseconds: 2000),
                  repeatPauseDuration: const Duration(milliseconds: 100),
                  repeat: true,
                  child: IconButton(
                    onPressed: _listen,
                    icon: Icon(_isListening ? Icons.mic : Icons.mic_none, color: Colors.amberAccent[100],
                       size: 25,
                    ),

                  ),
                ),

                title: Container(
                  height: MediaQuery.of(context).size.height*0.05,
                  decoration: BoxDecoration(

                    borderRadius: BorderRadius.all(Radius.circular(
                        15)),
                    color: Color.fromRGBO(220, 220, 220, 100),
                  ),

                  child: Container(
                    //padding: const EdgeInsets.all(),

                   padding: EdgeInsets.only(left:MediaQuery.of(context).size.width*0.02,right: MediaQuery.of(context).size.width*0.02 ),
                    child: TextFormField(

keyboardType: TextInputType.multiline,
                      //maxLines: null,
                      controller: messageInsert,
                      decoration: InputDecoration(
                        isDense: true,
                        hintText: "Ask Manavta",
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
                        response(messageInsert.text);
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

  void _listen() async {
    if (!_isListening) {
      bool available = await _speech.initialize(
        onStatus: (val) => print('onStatus: $val'),
        onError: (val) => print('onError: $val'),
      );
      if (available) {
        setState(() => _isListening = true);
        _speech.listen(
          onResult: (val) => setState(() {
            _text = val.recognizedWords;

            if (val.hasConfidenceRating && val.confidence > 0) {
              _confidence = val.confidence;
            }
          }),
        );
      }
    } else {

      setState(() {
        _isListening=false;
showDialog(context: context, barrierDismissible: true,builder: (_)=>
  AlertDialog(

    title:Container(
        padding: EdgeInsets.all(10),
        child: Text(_text)),
    actions: [
      TextButton(onPressed: (){

          setState(() {
            messsages.insert(0,
                {"data": 1, "message": _text});
          });
          response(_text.toString());
          messageInsert.clear();
          Navigator.pop(context);
        // FocusScopeNode currentFocus
        // FocusScope.of(context);
        // if (!currentFocus.hasPrimaryFocus) {
        //   currentFocus.unfocus();
        // }
      }, child: Text('Send Question')),
      TextButton(onPressed: (){
        Navigator.pop(context);
      }, child: Text('Retry')),
    ],
  ),
);
        print(_text);

      });
      _speech.stop();



    }
  }

}