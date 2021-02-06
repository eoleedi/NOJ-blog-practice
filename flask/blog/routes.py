from flask import render_template, request,session, g, flash, redirect, url_for, session
import os
from blog import app
from blog.schema import *
from blog.auth import login_required



@app.route('/', methods=['GET'])
def home():
    connect(os.environ['MONGODB_DATABASE'], host='mongodb', port=27017, username=os.environ['MONGODB_USERNAME'], password=os.environ['MONGODB_PASSWORD'])
    posts = Posts.objects(isPublic=True)
    return render_template('home.html', value=posts)

@app.route('/setting', methods=['GET', 'POST'])
@login_required
def setting():
    if request.method == 'GET':
        return render_template('setting.html')
    elif request.method == 'POST':
        connect(os.environ['MONGODB_DATABASE'], host='mongodb', port=27017, username=os.environ['MONGODB_USERNAME'], password=os.environ['MONGODB_PASSWORD'])
        user_search = Users.objects(username=session.get('user_id'))
        if user_search.count() == 1:
            user = user_search[0]
            user.nickname = request.form['nickname']
            user.save()
            return 'success'
        else:
            return 'failed'

@app.route('/post', methods=['GET','POST'])
@login_required
def post():
    if request.method == 'POST':
        connect(os.environ['MONGODB_DATABASE'], host='mongodb', port=27017, username=os.environ['MONGODB_USERNAME'], password=os.environ['MONGODB_PASSWORD'])
        
        post = Posts(
            title=request.form['title'],
            author=g.user['username'],
            content=request.form['content'],
            isPublic=request.form.get('isPublic')
        )
        post.save()
        return "success"
    else:
        return render_template('post.html')

@app.route('/profile/<id>')
def profile(id):
    connect(os.environ['MONGODB_DATABASE'], host='mongodb', port=27017, username=os.environ['MONGODB_USERNAME'], password=os.environ['MONGODB_PASSWORD'])
    user = Users.objects(username=id)
    profile = {'username': '', 'nickname': ''}
    if user.count() == 1:
        profile['username'] = user[0].username
        profile['nickname'] = user[0].nickname
        return render_template('profile.html', value=profile)
    else:
        return 'Profile not found.'

    