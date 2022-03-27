from flask import Flask
from flask_mongoengine import MongoEngine
import json
import toml

app = Flask(__name__)

config = toml.load("config.toml")

app.secret_key = config["secretkey"]
app.config["MONGODB_SETTINGS"] = {'DB': config["database"], "host": config["database-host"]}

db = MongoEngine(app)

class Diseases(db.Document):
    disease = db.StringField()
    description = db.StringField()
    departments = db.ListField(db.StringField())
    cure = db.ListField(db.StringField())
    def to_json(self):
        return {"disease": self.disease, "description": self.description, "departments": self.departments, "cure": self.cure}

def diseases_with_name(_, info, disease):
    return Diseases.objects(disease=disease).first()