from flask import render_template, request,session, g
import os
from blog import app
from blog.schema import *



@app.route('/', methods=['GET'])
def home():
    connect(os.environ['MONGODB_DATABASE'], host='mongodb', port=27017, username=os.environ['MONGODB_USERNAME'], password=os.environ['MONGODB_PASSWORD'])
    posts = Posts.objects(isPublic=True)
    return render_template('home.html', value=posts)

@app.route('/setting', methods=['GET'])
def setting():
    return render_template('setting.html')

@app.route('/post', methods=['GET','POST'])
def post():
    if request.method == 'POST':
        connect(os.environ['MONGODB_DATABASE'], host='mongodb', port=27017, username=os.environ['MONGODB_USERNAME'], password=os.environ['MONGODB_PASSWORD'])
        
        post = Posts(
            title=request.form['title'],
            author=g.user['username'],
            content=request.form['content'],
            isPublic=request.form['isPublic']
        )
        post.save()
        return "success"
    else:
        return render_template('post.html')

    