from flask import render_template, Flask, request, flash, redirect, url_for, session
from hashlib import pbkdf2_hmac

from blog import app
from blog.db import get_db


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.users.find({'username': username}) != '':
            error = 'Username has been used.'
        else:
            db.users.insert_one(
                {
                    'username': username,
                    'password': pbkdf2_hmac('sha512', password)
                }
            )
            return redirect(url_for('login'))
        flash(error)
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method = 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        user = db.users.find(
            {'username': username}
        )

        if user is None:
            error = 'User not exist.'
        elif user.password != pbkdf2_hmac('sha512', password):
            error = 'Incorrect password.'
        else:
            session.clear()
            session['user_id'] = user.username
    render_template('login.html')

        