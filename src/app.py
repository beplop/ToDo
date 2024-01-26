import os
from datetime import datetime
from functools import reduce

from flask import Flask, request, redirect, render_template, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import DictCursor

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from forms import LoginForm, RegisterForm
from UserLogin import UserLogin

####


####
load_dotenv()

template_dir = os.path.abspath('../templates/')
app = Flask(__name__, template_folder=template_dir)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
print(os.getenv('SECRET_KEY'))
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://admin:admin@192.168.99.100:6500/flask_todo_db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = "Вы не авторизованы"
login_manager.login_message_category = "success"


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(75), nullable=False, unique=True)
    password = db.Column(db.String(250), nullable=False)

    def __repr__(self):
        return f"<users {self.id}>"


class Notes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    text = db.Column(db.Text, nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    scheduled_on = db.Column(db.Integer, nullable=False, default=1)
    # 1 - сегодня, 2 - завтра, 3 - на этой неделе, 4 - бессрочно
    is_archived = db.Column(db.Boolean, default=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return f"<notes {self.id}>"


@login_manager.user_loader
def load_user(user_id):
    print("load_user")  # логирование сделай
    return UserLogin().fromDB(user_id, Users)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Вы вышли из аккаунта", "success")
    return redirect(url_for('login'))


# with app.app_context():
#     db.create_all()

# db.session.add(Users('admin@example.com', '123'))
# db.session.add(Users('guest@example.com', '123'))
# db.session.commit()
#
# users = Users.query.all()
# print(users)


# conn = psycopg2.connect(dbname='flask_todo_db', user='admin',
#                         password='admin', host='192.168.99.100', port='6500')


@app.route('/')
@login_required
def index():
    tasks1 = Notes.query.filter_by(scheduled_on=1, is_archived=False, user_id=current_user.get_id()).all()
    tasks2 = Notes.query.filter_by(scheduled_on=2, is_archived=False, user_id=current_user.get_id()).all()
    tasks3 = Notes.query.filter_by(scheduled_on=3, is_archived=False, user_id=current_user.get_id()).all()
    tasks4 = Notes.query.filter_by(scheduled_on=4, is_archived=False, user_id=current_user.get_id()).all()
    #
    email = current_user.get_email()
    #
    return render_template('index.html', title='Задачи', tasks1=tasks1, tasks2=tasks2, tasks3=tasks3, tasks4=tasks4,
                           email=email)


@app.route('/add', methods=['POST'])
@login_required
def add_task():
    # task1 = request.form.get('task1')
    # task2 = request.form.get('task2')
    # task3 = request.form.get('task3')
    # task4 = request.form.get('task4')
    tasks = [(1, request.form.get('task1')), (2, request.form.get('task2')), (3, request.form.get('task3')),
             (4, request.form.get('task4'))]

    task = reduce(lambda a, b: a if a[1] != None else b, tasks)

    # reduce func
    if task:
        try:
            # u = Users(email='abc@mail.ru', password='12345')
            #
            # db.session.add(u)
            # db.session.flush()

            # n = Notes(title=task1, user_id=u.id, scheduled_on=1)
            n = Notes(title=task[1], user_id=current_user.get_id(), scheduled_on=task[0], is_archived=False)
            db.session.add(n)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Ошибка добавления в БД {e}")

        # cursor = conn.cursor()
        # cursor.execute("INSERT INTO test.test_table (txt, title) VALUES (%s, %s)", (task, 'no title'))
        # conn.commit()
    # elif task2:
    #     try:
    #         # u = Users(email='bca@mail.ru', password='54321')
    #         #
    #         # db.session.add(u)
    #         # db.session.flush()
    #
    #         # n = Notes(title=task2, user_id=u.id, scheduled_on=2)
    #         n = Notes(title=task2, user_id=3, scheduled_on=2, is_archived=False)
    #         db.session.add(n)
    #         db.session.commit()
    #     except:
    #         db.session.rollback()
    #         print("Ошибка добавления в БД")

    return redirect('/')


@app.route('/detail/<int:task_id>')
@login_required
def detail_view_task(task_id):
    task = Notes.query.get(task_id)
    return render_template('detail.html', title=task.title, task=task)


@app.route('/update/<int:task_id>', methods=['POST'])
@login_required
def update_task(task_id):
    new_title = request.form.get('task_title')
    new_text = request.form.get('task_text')
    new_scheduled_on = request.form.get('task_scheduled_on')
    if new_title:
        try:
            task = Notes.query.get(task_id)
            task.title = new_title
            task.scheduled_on = new_scheduled_on

            if new_text:
                task.text = new_text

            db.session.commit()
        except:
            db.session.rollback()
            print("Ошибка обновления записи в БД")
    return redirect('/')


@app.route('/remove/<int:task_id>')
@login_required
def remove_task(task_id):
    try:
        task_to_remove = Notes.query.get(task_id)
        db.session.delete(task_to_remove)
        db.session.commit()
    except:
        db.session.rollback()
        print("Ошибка удаления из БД")
    return redirect('/')


@app.route('/to_archive/<int:task_id>')
@login_required
def task_to_archive(task_id):
    try:
        task_to_archive = Notes.query.get(task_id)
        task_to_archive.is_archived = not task_to_archive.is_archived
        db.session.commit()
    except:
        db.session.rollback()
        print("Ошибка добавления в архив записи")
    return redirect('/')


@app.route('/archive/')
@login_required
def archive():
    archived_tasks = Notes.query.filter_by(is_archived=True, user_id=current_user.get_id()).all()
    return render_template('archive.html', title='Архив', archived_tasks=archived_tasks)


@app.route("/login", methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter(Users.email == form.email.data).first()
        if user and check_password_hash(user.password, form.psw.data):
            userlogin = UserLogin().create(user)
            rm = form.remember.data
            login_user(userlogin, remember=rm)
            # login_user(userlogin)
            # return redirect(request.args.get("next") or url_for("profile"))
            return redirect(request.args.get("next") or url_for('index'))

        flash("Неверная пара логин/пароль", "error")
    return render_template("login.html", form=form)


@app.route("/register", methods=["POST", "GET"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        try:
            if Users.query.filter(Users.email == form.email.data).first():
                flash("Такой пользователь уже существует", "error")
                return redirect(url_for('register'))
            else:
                hash_psw = generate_password_hash(request.form['psw'])
                u = Users(email=form.email.data, password=hash_psw)
                db.session.add(u)
                db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(e)
        flash("Вы успешно зарегистрированы", "success")
        return redirect(url_for('login'))
    else:
        if form.is_submitted():
            # log
            flash("Ошибка при регистрации", "error")
            print('Даннные формы введены неверно или что-то пошло не так')
    return render_template("register.html", form=form)


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
