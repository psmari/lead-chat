# from lead import Lead
from database.messages import Messages
from database.lead import Lead
from mongoengine.document import Document
from mongoengine.fields import DateTimeField, ReferenceField, StringField


class Chat(Document):
    lead_id = ReferenceField(Lead)
    send = ReferenceField(Messages)
    receive = StringField()
    date = DateTimeField()