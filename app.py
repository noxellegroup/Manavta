from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from flask_socketio import SocketIO
from flask_mongoengine import MongoEngine
import toml
import pyttsx3
# Classifier
from classifier import intent_identifier
# Symptoms-Disease
from symptoms_disease_predictor import symptoms_disease_predict
# Models
from models import db, Diseases
# Spell checker
from spellchecker import SpellChecker

config = toml.load("config.toml")

app = Flask(__name__)

app.secret_key = 'canada$God7972#'
socketio = SocketIO(app)

app.config["MONGODB_SETTINGS"] = {'DB': config["database"], "host":config["database-host"]}

db = MongoEngine(app)

spell = SpellChecker()

class Diseases(db.Document):
    disease = db.StringField()
    description = db.StringField()
    def to_json(self):
        return {"disease": self.disease, "description": self.description}

@app.route('/')
def sessions():
    return render_template('index.html', version=config["version"])

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
            else:
                data["response"] = "Coming soon."

            socketio.emit('bot response', data, callback=messageReceived)
            engine = pyttsx3.init()
            engine.say(data["response"])
            engine.runAndWait()
            engine.stop()

        except Exception as e:
            pass

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', debug=True)