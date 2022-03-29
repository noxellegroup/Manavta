from flask import Flask
from flask_mongoengine import MongoEngine
import json
import toml
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

app = Flask(__name__)

config = toml.load("config.toml")

app.secret_key = config["secretkey"]
app.config["MONGODB_SETTINGS"] = {'DB': config["database"], "host": config["database-host"]}

db = MongoEngine(app)

spell = SpellChecker()

class Diseases(db.Document):
    disease = db.StringField()
    description = db.StringField()
    departments = db.ListField(db.StringField())
    cure = db.ListField(db.StringField())
    def to_json(self):
        return {"disease": self.disease, "description": self.description, "departments": self.departments, "cure": self.cure}

def diseases_with_name(_, info, disease):
    return Diseases.objects(disease=disease).first()

def diseases_with_id(_, info, id):
    return Diseases.objects(id=id).first()

def chatbot_dialogue(_, info, message):
    try:
        data = {"message": message}
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
                            message += f"Here's what I know about {disease}: {Diseases.objects(disease=disease).first().description} and "
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
                            message += f"{disease} belongs to: {result} and "
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
                            message += f"To treat {disease} you need: {result} and "
                        else:
                            info += f"To treat {disease} you need: {result}"
                            message += f"To treat {disease} you need: {result}"
                data["response"] = info
            else:
                data["response"] = "Coming soon."
                message = data["response"]
        return {"response": message}
    except Exception as e:
        print(e)