from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, FileField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, Length
from flask_wtf.file import FileAllowed

class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')

class MaterialForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired(), Length(max=200)])
    content = TextAreaField('Содержание', validators=[DataRequired()])
    category = SelectField('Категория', choices=[
        ('consultation', 'Консультация'),
        ('scenario', 'Сценарий праздника'),
        ('methodical', 'Методическая разработка'),
        ('article', 'Статья')
    ], validators=[DataRequired()])
    target_audience = SelectField('Для кого', choices=[
        ('teachers', 'Педагоги'),
        ('parents', 'Родители'),
        ('all', 'Все')
    ], validators=[DataRequired()])
    file = FileField('Файл', validators=[FileAllowed(['pdf', 'doc', 'docx', 'jpg', 'png'], 'Только документы и изображения!')])