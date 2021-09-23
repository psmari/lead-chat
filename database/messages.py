
from mongoengine.document import Document
from mongoengine.fields import StringField

class Messages(Document):
    text = StringField()
    type = StringField()
    number = StringField()