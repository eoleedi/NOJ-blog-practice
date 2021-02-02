from flask import render_template, Flask, request, flash, redirect, url_for, session, g
from werkzeug.security import generate_password_hash, check_password_hash
import functools
import os

from mongoengine import *
from blog import app
from blog.db import get_db
from blog.schema import *
from blog.routes import *

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        connect(os.environ['MONGODB_DATABASE'], host='mongodb', port=27017, username=os.environ['MONGODB_USERNAME'], password=os.environ['MONGODB_PASSWORD'])
        user = Users(
            username=request.form['username'],
            password=generate_password_hash(request.form['password']),
            nickname=request.form['username']
        )

        error = None

        if not user.username:
            error = 'Username is required.'
        elif not user.password:
            error = 'Password is required.'
        elif Users.objects(username=user.username).count() != 0:
            error = 'Username has been used. '
        else:
            user.save()
            return redirect(url_for('login'))
        flash(error)
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        connect(os.environ['MONGODB_DATABASE'], host='mongodb', port=27017, username=os.environ['MONGODB_USERNAME'], password=os.environ['MONGODB_PASSWORD'])
        user = Users(
            username=request.form['username'],
            password=request.form['password'],
        )

        error = None

        user_search = Users.objects(username=user.username)

        if len(user_search) == 0:
            error = 'User not exist.'
        elif len(user_search) != 1:
            error = 'System Error. Mutiple username in system.'
        elif check_password_hash(user.password, user_search[0].password):
            error = 'Incorrect password.'
        else:
            session.clear()
            session['user_id'] = user.username
            return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.before_request
def load_logged_in_user():
    
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        connect(os.environ['MONGODB_DATABASE'], host='mongodb', port=27017, username=os.environ['MONGODB_USERNAME'], password=os.environ['MONGODB_PASSWORD'])
        g.user = Users.objects(username=user_id)[0]
        

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('login'))
        
        return view(**kwargs)

    return wrapped_view

        