from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from flask_session import Session
from flask_socketio import SocketIO
from flask_mongoengine import MongoEngine
from flask_github import GitHub
from ariadne import graphql_sync, make_executable_schema, load_schema_from_path, ObjectType, QueryType
from ariadne.constants import PLAYGROUND_HTML
import toml
import os
import resolvers as r
import pyttsx3
import platform
# Classifier
from classifier import intent_identifier
# Symptoms-Disease
from symptoms_disease_predictor import symptoms_disease_predict
# Accompany-Disease
from accompany_disease_predictor import accompany_disease_predict
# General-Intent
from general_intent import general_intent_handler
# Models
from models import db, Diseases
# Spell checker
from spellchecker import SpellChecker
# Punctuation Handler
from punctuation_handler import punctuation_handler

config = toml.load("config.toml")

app = Flask(__name__)
port = int(os.environ.get('PORT', 5000))

app.secret_key = config["secretkey"]
socketio = SocketIO(app)

app.config["MONGODB_SETTINGS"] = {'DB': config["database"], "host": config["database-host"]}
app.config["GITHUB_CLIENT_ID"] = config["github-client-ID"]
app.config["GITHUB_CLIENT_SECRET"] = config["github-client-secret"]
app.config['SESSION_TYPE'] = 'filesystem'

Session(app)

db = MongoEngine(app)

github = GitHub(app)

spell = SpellChecker()

type_defs = load_schema_from_path('schema.graphql')

query = QueryType()
gqlDiseases = ObjectType('Diseases')
gqlDialogue = ObjectType('Dialogue')

query.set_field('diseases_with_name', r.diseases_with_name)
query.set_field('diseases_with_id', r.diseases_with_id)
query.set_field('chatbot_dialogue', r.chatbot_dialogue)

schema = make_executable_schema(type_defs, [gqlDiseases, gqlDialogue, query])

class Diseases(db.Document):
    disease = db.StringField()
    description = db.StringField()
    departments = db.ListField(db.StringField())
    cure = db.ListField(db.StringField())
    def to_json(self):
        return {"disease": self.disease, "description": self.description, "departments": self.departments, "cure": self.cure}

@app.route('/graphql', methods=['GET'])
def playground():
    return PLAYGROUND_HTML, 200

@app.route('/graphql', methods=['POST'])
def graphql_server():
    data = request.get_json()
    success, result = graphql_sync(schema, data, context_value=None, debug=app.debug)
    status_code = 200 if success else 400
    return jsonify(result), status_code

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
            original = data["message"]
            data["message"] = punctuation_handler(data["message"])
            tokens = data["message"].split(" ")
            misspelled = spell.unknown(tokens)
            if len(misspelled)!=0:
                for word in misspelled:
                    data["message"] = data["message"].replace(word, spell.correction(word))

            intent = intent_identifier(data["message"])

            message = f""

            if not intent:
                data["response"] = general_intent_handler(original)
                message = data["response"]
            else:
                intent_type = intent["question_types"][0]

                if intent_type == "symptom_disease":
                    symptoms = []
                    for i in intent["args"]:
                        if "symptom" in intent["args"][i]:
                            symptoms.append(i)
                    disease = symptoms_disease_predict(symptoms)
                    data["response"] = f"You most likely have {disease}."
                    message = data["response"]
                elif intent_type == "disease_desc":
                    diseases = []
                    for i in intent["args"]:
                        if "disease" in intent["args"][i]:
                            diseases.append(i)
                    info = f""
                    for index, disease in enumerate(diseases):
                        if (len(diseases)==1):
                            info += f"Here's what I know about {disease}: {Diseases.objects(disease=disease).first().description}"
                            message += f"Here's what I know about {disease}: {Diseases.objects(disease=disease).first().description}"
                        else:
                            if (index!=(len(diseases)-1)):
                                info += f"Here's what I know about {disease}: {Diseases.objects(disease=disease).first().description} <br>"
                                message += f"Here's what I know about {disease}: {Diseases.objects(disease=disease).first().description} and"
                            else:
                                info += f"Here's what I know about {disease}: {Diseases.objects(disease=disease).first().description}"
                                message += f"Here's what I know about {disease}: {Diseases.objects(disease=disease).first().description}"
                    data["response"] = info
                elif intent_type == "disease_accompany":
                    accompanies = []
                    for i in intent["args"]:
                        if "disease" in intent["args"][i]:
                            accompanies.append(i)
                    disease = accompany_disease_predict(accompanies)
                    data["response"] = f"You can develop complications such as {disease}."
                    message = data["response"]
                elif intent_type == "disease_department":
                    diseases = []
                    for i in intent["args"]:
                        if "disease" in intent["args"][i]:
                            diseases.append(i)
                    info = f""
                    for index, disease in enumerate(diseases):
                        departments = Diseases.objects(disease=disease).first().departments
                        disease = disease.capitalize()
                        if (len(departments)==1):
                            result = departments[0].capitalize()
                        elif (len(departments)==2):
                            result = f"{departments[0].capitalize()} ({departments[1].capitalize()})"
                        if (len(diseases)==1):
                            info += f"{disease} belongs to: {result}"
                            message += f"{disease} belongs to: {result}"
                        else:
                            if (index!=(len(diseases)-1)):
                                info += f"{disease} belongs to: {result} <br>"
                                message += f"{disease} belongs to: {result} and"
                            else:
                                info += f"{disease} belongs to: {result}"
                                message += f"{disease} belongs to: {result}"
                    data["response"] = info
                elif intent_type == "disease_cure":
                    diseases = []
                    for i in intent["args"]:
                        if "disease" in intent["args"][i]:
                            diseases.append(i)
                    info = f""
                    for index, disease in enumerate(diseases):
                        cures = Diseases.objects(disease=disease).first().cure
                        if (len(cures)==1):
                            result = cures[0].capitalize()
                        elif (len(cures)>1):
                            result = ", ".join(cures).capitalize()
                        if (len(diseases)==1):
                            info += f"To treat {disease} you need: {result}"
                            message += f"To treat {disease} you need: {result}"
                        else:
                            if (index!=(len(diseases)-1)):
                                info += f"To treat {disease} you need: {result} <br>"
                                message += f"To treat {disease} you need: {result} and"
                            else:
                                info += f"To treat {disease} you need: {result}"
                                message += f"To treat {disease} you need: {result}"
                    data["response"] = info
                else:
                    data["response"] = "Coming soon."
                    message = data["response"]

            socketio.emit('bot response', data, callback=messageReceived)

            if (platform.system()=="Windows"):
                engine = pyttsx3.init()
                engine.say(message)
                engine.runAndWait()
                engine.stop()

        except Exception as e:
           print(e)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=port, debug=True)