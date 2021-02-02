from mongoengine import *
import datetime

class Users(Document):
    username = StringField(max_length=100, required=True)
    password = StringField(max_length=100, required=True)
    nickname = StringField(max_length=100, default=username)
    posts = ListField()

class Posts(Document):
    title = StringField(max_length=100, required=True)
    author = StringField(max_length=100, required=True)
    content = StringField(max_length=1000)
    isPublic = BooleanField(required=True, default=False)

