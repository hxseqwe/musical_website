from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, FileField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Optional
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

class EventForm(FlaskForm):
    title = StringField('Название мероприятия', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Описание')
    event_date = StringField('Дата мероприятия (ГГГГ-ММ-ДД)', validators=[DataRequired(), Length(max=10)])
    event_time = StringField('Время проведения', validators=[Length(max=50)])
    event_type = SelectField('Тип мероприятия', choices=[
        ('утренник', 'Утренник'),
        ('занятие', 'Занятие'),
        ('собрание', 'Родительское собрание'),
        ('мероприятие', 'Мероприятие'),
        ('репетиция', 'Репетиция'),
        ('конкурс', 'Конкурс'),
        ('другое', 'Другое')
    ], validators=[DataRequired()])
    age_group = SelectField('Возрастная группа', choices=[
        ('младшая', 'Младшая группа (3-4 года)'),
        ('средняя', 'Средняя группа (4-5 лет)'),
        ('старшая', 'Старшая группа (5-6 лет)'),
        ('подготовительная', 'Подготовительная группа (6-7 лет)'),
        ('все', 'Все группы')
    ], validators=[DataRequired()])
    location = StringField('Место проведения', validators=[Length(max=100)])
    participants = TextAreaField('Участники')
    materials = TextAreaField('Необходимые материалы')
    notes = TextAreaField('Заметки')
    status = SelectField('Статус', choices=[
        ('запланировано', 'Запланировано'),
        ('в_процессе', 'В процессе'),
        ('завершено', 'Завершено'),
        ('отменено', 'Отменено')
    ])
    submit = SubmitField('Сохранить мероприятие')