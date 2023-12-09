import os

from flask import Flask, request, redirect, render_template
import psycopg2
from psycopg2.extras import DictCursor

template_dir = os.path.abspath('../templates/')
app = Flask(__name__, template_folder=template_dir)

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

