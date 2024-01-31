from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo


class LoginForm(FlaskForm):
    email = StringField("Email: ", validators=[Email("Некорректный email")])
    psw = PasswordField("Пароль: ", validators=[DataRequired(), Length(min=4, max=75,
                                                                       message="Пароль должен быть от 4 до 75 символов")])
    remember = BooleanField("Запомнить", default=False)
    submit = SubmitField("Войти")


class RegisterForm(FlaskForm):
    email = StringField("Email: ", validators=[Email("Некорректный email")])
    psw = PasswordField("Пароль: ", validators=[DataRequired(),
                                                Length(min=4, max=75,
                                                       message="Пароль должен быть от 4 до 75 символов")])

    psw2 = PasswordField("Повтор пароля: ", validators=[DataRequired(), EqualTo('psw', message="Пароли не совпадают")])
    submit = SubmitField("Регистрация")


class PasswordUpdateForm(FlaskForm):
    psw_current = PasswordField("Текущий пароль: ", validators=[DataRequired(),
                                                                Length(min=4, max=75,
                                                                       message="Пароль должен быть от 4 до 75 символов")])
    psw_new = PasswordField("Новый пароль: ", validators=[DataRequired(),
                                                          Length(min=4, max=75,
                                                                 message="Пароль должен быть от 4 до 75 символов")])

    psw_new2 = PasswordField("Повторите пароль: ",
                             validators=[DataRequired(), EqualTo('psw_new', message="Пароли не совпадают")])
    submit = SubmitField("Сменить пароль")


class PasswordRecoveryForm(FlaskForm):
    code = StringField("Код, полученный на e-mail: ", validators=[DataRequired(),
                                                                  Length(min=4, max=4,
                                                                         message="Код должен состоять из четырёх цифр")])
    psw_new = PasswordField("Новый пароль: ", validators=[DataRequired(),
                                                          Length(min=4, max=75,
                                                                 message="Пароль должен быть от 4 до 75 символов")])

    psw_new2 = PasswordField("Повторите пароль: ",
                             validators=[DataRequired(), EqualTo('psw_new', message="Пароли не совпадают")])
    submit = SubmitField("Сменить пароль")


class GetEmailForm(FlaskForm):
    email = StringField("Email: ", validators=[Email("Некорректный email")])
    submit = SubmitField("Далее")
