from flask import render_template, request
from blog import app
from blog import db


@app.route('/', methods=['GET'])
def hello():
    return 'Hello world.'

@app.route('/post', methods=['GET','POST'])
def post():
    if request.method == 'POST':
        datab = db.get_db()
        datab.news.insert_one(
            {
                'title': 'test',
                'author': 'name',
                'content': 'content',
                'is_public': True
            }
        )
        return "success"
    else:
        return render_template('post.html')
    