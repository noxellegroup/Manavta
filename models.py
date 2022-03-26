from flask_mongoengine import MongoEngine

db = MongoEngine()

class Diseases(db.Document):
    ''' Class for defining structure of diseases and their corresponding attributes
    '''
    disease = db.StringField(required=True)
    description = db.StringField(required=True)
    departments = db.ListField(db.StringField(required=True))
    cure = db.ListField(db.StringField(required=True))

    meta = {
        'collection': 'disease-description', # collection name
        'ordering': ['-score'], # default ordering
        'auto_create_index': False, # MongoEngine will not create index
    }