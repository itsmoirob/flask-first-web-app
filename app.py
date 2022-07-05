import datetime
from markupsafe import escape
from flask import Flask, abort, render_template

app = Flask(__name__)

messages = [{'title': 'Message one', 'content': 'Message one content'},
            {'title': 'Message one', 'content': 'Message two content'}]


@app.route('/')
@app.route('/index')
def hello():
    return '<h1>Hello Arthur!!</h1>'


@app.route('/about/')
def about():
    return '<h3>This is a Flask web app</h3>'


@app.route('/capitalize/<word>')
def capitalize(word):
    return '<h1>{}</h1>'.format(escape(word.capitalize()))


@app.route('/add/<int:n1>/<int:n2>')
def add(n1, n2):
    return '<h1>{}</h1>'.format(n1 + n2)


@app.route('/user/<int:user_id>')
def greet_user(user_id):
    users = ['Arthur', 'Emma', 'Robbie']
    try:
        return '<h2>Hi {}</h2>'.format(users[user_id])
    except IndexError:
        abort(404)


@app.route('/template/')
def template():
    return render_template('hello.html', utc_dt=datetime.datetime.utcnow())


@app.route('/template-about/')
def template_about():
    return render_template('about.html')


@app.route('/comments/')
def comments():
    comments = ['This is the first comment.',
                'This is the second comment.',
                'This is the third comment.',
                'This is the fourth comment.'
                ]

    return render_template('comments.html', comments=comments)


@app.route('/web-form/')
def web_form():
    return render_template('web-form.html', messages=messages)


@app.route('/create/', methods=('GET', 'POST'))
def create():
    return render_template('create.html')
