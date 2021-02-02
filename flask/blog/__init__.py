from flask import Flask
import os

app = Flask(__name__)
app.secret_key = os.environ['FLASK_SECRET_KEY']
from blog import routes
from blog import auth
from blog import schema






    


