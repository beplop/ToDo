import os
from datetime import datetime

from flask import Flask, request, redirect, render_template
import psycopg2
from psycopg2.extras import DictCursor

from flask_sqlalchemy import SQLAlchemy

template_dir = os.path.abspath('../templates/')
app = Flask(__name__, template_folder=template_dir)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://admin:admin@192.168.99.100:6500/flask_todo_db'
db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(500), nullable=False)

    def __repr__(self):
        return f"<users {self.id}>"

class Notes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    text = db.Column(db.Text, nullable=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return f"<profiles {self.id}>"

with app.app_context():
    db.create_all()

    # db.session.add(Users('admin@example.com', '123'))
    # db.session.add(Users('guest@example.com', '123'))
    # db.session.commit()
    #
    # users = Users.query.all()
    # print(users)


tasks = []  # Список задач


conn = psycopg2.connect(dbname='flask_todo_db', user='admin',
                        password='admin', host='192.168.99.100', port='6500')

@app.route('/')
def index():
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    task = request.form.get('task')
    if task:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO test.test_table (txt, title) VALUES (%s, %s)", (task, 'no title'))
        conn.commit()

    return redirect('/')

@app.route('/remove/<int:index>')
def remove_task(index):
    if 0 <= index < len(tasks):
        del tasks[index]
    return redirect('/')

# @app.route('/')
# def hello_world():  # put application's code here
#     conn = psycopg2.connect(dbname='flask_todo_db', user='admin',
#                             password='admin', host='192.168.99.100', port='6500')
#     # conn = psycopg2.connect(dbname='flask_todo_db', user='admin',
#     #                         password='admin', host='172.20.0.3', port='5432')
#     cursor = conn.cursor(cursor_factory=DictCursor)
#     cursor.execute('SELECT * FROM test.test_table')
#     records = cursor.fetchone()
#     cursor.close()
#     conn.close()
#     print(records[0])
#     return records[0]

    # return "hello world man! 12345678"



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int("5000"))

