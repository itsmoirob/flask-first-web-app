import datetime
import sqlite3
from markupsafe import escape
from flask import Flask, abort, render_template, request, url_for, flash, redirect
from forms import CourseForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '5272f00818210386d6e839c91c4bff24bb513081f86166da'


def get_db_connection():
    """Connection to the database"""
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
@app.route('/index')
def hello():
    """A route"""
    return '<h1>Hello Arthur!!</h1>'


@app.route('/about/')
def about():
    """A basic intro route"""
    return '<h3>This is a Flask web app</h3>'


@app.route('/capitalize/<word>')
def capitalize(word):
    """A route that uses paramaters"""
    return f"<h1>{escape(word.capitalize())}</h1>"


@app.route('/add/<int:n1>/<int:n2>')
def add(n_1, n_2):
    """A route that uses two paramaters"""
    return f"<h1>{n_1 + n_2}</h1>"


@app.route('/user/<int:user_id>')
def greet_user(user_id):
    """A route that shows error handle"""
    users = ['Arthur', 'Emma', 'Robbie']
    try:
        return f"<h2>Hi {users[user_id]}</h2>"
    except IndexError:
        abort(404)


@app.route('/template/')
def template():
    """A route with basic template"""
    return render_template('hello.html', utc_dt=datetime.datetime.utcnow())


@app.route('/template-about/')
def template_about():
    """A route with another basic template"""
    return render_template('about.html')


courses_list = [{
    'title': 'Python 101',
    'description': 'Learn Python basics',
    'price': 34,
    'available': True,
    'level': 'Beginner'
}]


@app.route('/course-form', methods=('GET', 'POST'))
def course_form():
    """A route for creating course with WTF form"""
    form = CourseForm()
    if form.validate_on_submit():
        courses_list.append({'title': form.title.data,
                             'description': form.description.data,
                             'price': form.price.data,
                             'available': form.available.data,
                             'level': form.level.data
                             })
        return redirect(url_for('courses'))

    return render_template('course-form.html', form=form)


@app.route('/courses/')
def courses():
    """A route for showing courses"""
    return render_template('courses.html', courses_list=courses_list)


@app.route('/sql-comments/')
def sql_comments():
    """A route with SQLite conn"""
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('sql-comments.html', posts=posts)


# @app.route('/create/', methods=('GET', 'POST'))
# def create():
#     """A route for showing and using webforms"""
#     if request.method == 'POST':
#         title = request.form['title']
#         content = request.form['content']

#         if not title:
#             flash('Title is required!')
#         elif not content:
#             flash('Content is require!')
#         else:
#             messages.append({'title': title, 'content': content})
#             return redirect(url_for('comments'))

#     return render_template('create.html')
