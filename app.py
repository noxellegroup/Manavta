from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from flask_socketio import SocketIO
import time
import json
# Classifier
from classifier import intent_identifier
# Symptoms-Disease
from symptoms_disease_predictor import symptoms_disease_predict
# Disease-Description
from disease_desc import disease_desc_display

app = Flask(__name__)

app.secret_key = 'canada$God7972#'
socketio = SocketIO(app)

@app.route('/')
def sessions():
    return render_template('index.html')

def messageReceived(methods=['GET', 'POST']):
    print('Message was received')
    
@socketio.on('user connect')
def user_connect(data, methods=['GET', 'POST']):
    data["user_name"] = "Manav"
    data["greet"] = "Hey there! I'm Manav, your personal health assistant. Ask me anything &#128512;"
    socketio.emit('bot greet', data, callback=messageReceived)
        
@socketio.on('user response')
def user_response(data, methods=['GET', 'POST']):
    socketio.emit('user response', data, callback=messageReceived)
    
    if "message" in data:
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
            for i in diseases:
                info += f"Here's what I know about {i}: " + disease_desc_display(i) + f" <br>"
            data["response"] = info
    
    socketio.emit('bot response', data, callback=messageReceived)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', debug=True)