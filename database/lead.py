
from mongoengine.document import Document
from mongoengine.fields import StringField

class Lead(Document):
    name = StringField()
    username_whats = StringField()
    phone = StringField()
    email = StringField()
    marca = StringField()
    site = StringField()