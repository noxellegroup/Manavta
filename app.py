from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from flask_session import Session
from flask_socketio import SocketIO
from flask_mongoengine import MongoEngine
from flask_github import GitHub
import toml
import pyttsx3
# Classifier
from classifier import intent_identifier
# Symptoms-Disease
from symptoms_disease_predictor import symptoms_disease_predict
# Accompany-Disease
from accompany_disease_predictor import accompany_disease_predict
# Models
from models import db, Diseases
# Spell checker
from spellchecker import SpellChecker

config = toml.load("config.toml")

app = Flask(__name__)

app.secret_key = config["secretkey"]
socketio = SocketIO(app)

app.config["MONGODB_SETTINGS"] = {'DB': config["database"], "host":config["database-host"]}
app.config["GITHUB_CLIENT_ID"] = config["github-client-ID"]
app.config["GITHUB_CLIENT_SECRET"] = config["github-client-secret"]
app.config['SESSION_TYPE'] = 'filesystem'

Session(app)

db = MongoEngine(app)

github = GitHub(app)

spell = SpellChecker()

class Diseases(db.Document):
    disease = db.StringField()
    description = db.StringField()
    def to_json(self):
        return {"disease": self.disease, "description": self.description}

@app.route('/')
def chat():
    if not session.get("username"):
        return redirect(url_for("login"))
    else:
        return render_template("index.html", version=config["version"], username=session["username"])

@app.route('/login')
def login():
    if not session.get("username"):
        return render_template("login.html")
    else:
        return redirect(url_for("chat"))

@app.route('/authorize')
def authorize():
    return github.authorize()

@github.access_token_getter
def token_getter():
    token = session["token"]
    if token is not None:
        return token

@app.route('/auth-callback')
@github.authorized_handler
def authorized(oauth_token):
    if oauth_token is None:
        # Login failed
        return redirect(url_for("login"))
    elif not session.get("username"):
        session["token"] = oauth_token
        user = github.get('/user')
        session["username"] = user['login']
        return redirect(url_for("chat"))
    elif session.get("username"):
        session["token"] = oauth_token
        user = github.get('/user')
        session["username"] = user['login']
        return redirect(url_for("chat"))

@app.route('/logout')
def logout():
    session["username"] = None
    return redirect(url_for("login"))

def messageReceived(methods=['GET', 'POST']):
    print('Message was received')
    
@socketio.on('user connect')
def user_connect(data, methods=['GET', 'POST']):
    data["user_name"] = "Manav"
    data["greet"] = "Hey there! I'm Manav, your personal health assistant. Ask me anything &#128512;"
    socketio.emit('bot greet', data, callback=messageReceived)
    engine = pyttsx3.init()
    engine.say(data["greet"][:len(data["greet"])-9])
    engine.runAndWait()
    engine.stop()
        
@socketio.on('user response')
def user_response(data, methods=['GET', 'POST']):
    socketio.emit('user response', data, callback=messageReceived)
    
    if "message" in data:
        try:
            tokens = data["message"].split(" ")
            misspelled = spell.unknown(tokens)
            if len(misspelled)!=0:
                corrected_tokens = []
                for word in misspelled:
                    corrected_tokens.append(spell.correction(word))
                data["message"] = " ".join(corrected_tokens)

            intent = intent_identifier(data["message"])
            intent_type = intent["question_types"][0]
            if intent_type == "symptom_disease":
                symptoms = []
                for i in intent["args"]:
                    if "symptom" in intent["args"][i]:
                        symptoms.append(i)
                disease = symptoms_disease_predict(symptoms)
                data["response"] = f"You most likely have {disease}."
            elif intent_type == "disease_desc":
                diseases = []
                for i in intent["args"]:
                    if "disease" in intent["args"][i]:
                        diseases.append(i)
                info = f""
                for disease in diseases:
                    info += f"Here's what I know about {disease}: {Diseases.objects(disease=disease).first().description} <br>"
                data["response"] = info
            elif intent_type == "disease_accompany":
                accompanies = []
                for i in intent["args"]:
                    if "disease" in intent["args"][i]:
                        accompanies.append(i)
                disease = accompany_disease_predict(accompanies)
                data["response"] = f"You can develop complications such as {disease}."
            else:
                data["response"] = "Coming soon."

            socketio.emit('bot response', data, callback=messageReceived)
            engine = pyttsx3.init()
            engine.say(data["response"])
            engine.runAndWait()
            engine.stop()

        except Exception as e:
           print(e)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', debug=True)