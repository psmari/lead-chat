import os
from mongoengine import connect

connect(os.getenv("MONGODB_URI"))