from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, FileField, PasswordField, BooleanField, SubmitField, DateField
from wtforms.validators import DataRequired, Length, Optional
from flask_wtf.file import FileAllowed, FileSize

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
    file = FileField('Файл', validators=[
        FileAllowed(['pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png'], 'Только документы и изображения!'),
        FileSize(max_size=10*1024*1024, message='Файл не должен превышать 10MB')
    ])

class EventForm(FlaskForm):
    title = StringField('Название мероприятия', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Описание')
    event_date = DateField('Дата мероприятия', format='%Y-%m-%d', validators=[DataRequired()])
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

class ContactForm(FlaskForm):
    name = StringField('Ваше имя', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    subject = SelectField('Тема сообщения', choices=[
        ('', 'Выберите тему'),
        ('Консультация по музыкальному развитию', 'Консультация по музыкальному развитию'),
        ('Вопрос по методическим материалам', 'Вопрос по методическим материалам'),
        ('Предложение о сотрудничестве', 'Предложение о сотрудничестве'),
        ('Обмен опытом', 'Обмен опытом'),
        ('Другое', 'Другое')
    ], validators=[DataRequired()])
    message = TextAreaField('Сообщение', validators=[DataRequired()])
    submit = SubmitField('Отправить сообщение')