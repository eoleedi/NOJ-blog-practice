from flask import render_template, request,session, g, flash, redirect, url_for, session
import os
from blog import app
from blog.schema import *
from blog.auth import login_required, load_logged_in_user



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
    
    try:
        user = Users.objects.exclude('password').get(username=id)
        posts = Posts.objects(author=id)
        profile = {'username': '', 'nickname': ''} 

        if session.get('user_id') == id:
            isSelfUser = True
        return render_template('profile.html', profile=user, posts=posts, isSelfUser=isSelfUser)
    except DoesNotExist:
        return 'Profile not found.'
    except MultipleObjectsReturned:
        return 'Multiple users have found. System error.'


@app.route('/posts/<id>')
def get_post_page(id):
    connect(os.environ['MONGODB_DATABASE'], host='mongodb', port=27017, username=os.environ['MONGODB_USERNAME'], password=os.environ['MONGODB_PASSWORD'])
    try:
        post = Posts.objects.get(id=id)
        if post.isPublic == True or session.get('user_id') == post.author:
            if post.isPublic:
                isPublic = "checked"
            else:
                isPublic = "unchecked"
            return render_template('post_page.html', post=post, isPublic=isPublic)
        else:
            return 'Permission denied'
    except DoesNotExist:
        return 'Post not found.'

@app.route('/modify/<id>', methods=['POST'])
@login_required
def modify_post(id):
    connect(os.environ['MONGODB_DATABASE'], host='mongodb', port=27017, username=os.environ['MONGODB_USERNAME'], password=os.environ['MONGODB_PASSWORD'])
    string_to_boolean = lambda string: string=='True' 
    
    try:
        post = Posts.objects.get(id=id)
        if g.user.username == post.author:
            post.update(
                title=request.form['title'],
                author=session.get('user_id'),
                content=request.form['content'],
                isPublic=string_to_boolean(request.form.get('isPublic')) 
            )
            return "Success"
        else:
            return "Permission Denied." + g.user.username
    except DoesNotExist:  
        return "Post not found. Can't not modify"
    except MultipleObjectsReturned:
        return "Mutliple posts found. System Error"
    




    