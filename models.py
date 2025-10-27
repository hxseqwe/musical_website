from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime, timezone
import os

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

class Material(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    target_audience = db.Column(db.String(50), nullable=False)
    created_date = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    file_path = db.Column(db.String(300))
    is_published = db.Column(db.Boolean, default=True)

class PageVisit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    page = db.Column(db.String(100), nullable=False)
    visit_date = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    ip_address = db.Column(db.String(45))

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    event_date = db.Column(db.DateTime, nullable=False)
    event_time = db.Column(db.String(50))
    event_type = db.Column(db.String(50))
    age_group = db.Column(db.String(20))
    location = db.Column(db.String(100))
    participants = db.Column(db.Text)
    materials = db.Column(db.Text)
    notes = db.Column(db.Text)
    status = db.Column(db.String(20), default='запланировано') 
    created_date = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_date = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f'<Event {self.title} {self.event_date}>'
    
    @property
    def status_display(self):
        status_map = {
            'запланировано': 'Запланировано',
            'в_процессе': 'В процессе',
            'завершено': 'Завершено',
            'отменено': 'Отменено'
        }
        return status_map.get(self.status, self.status)
    
    @property
    def status_color(self):
        color_map = {
            'запланировано': 'primary',
            'в_процессе': 'warning', 
            'завершено': 'success',
            'отменено': 'danger'
        }
        return color_map.get(self.status, 'secondary')
    
    @property
    def event_type_display(self):
        type_map = {
            'утренник': 'Утренник',
            'занятие': 'Занятие',
            'собрание': 'Родительское собрание',
            'мероприятие': 'Мероприятие',
            'репетиция': 'Репетиция',
            'конкурс': 'Конкурс',
            'другое': 'Другое'
        }
        return type_map.get(self.event_type, self.event_type)
    
    @property
    def age_group_display(self):
        group_map = {
            'младшая': 'Младшая группа (3-4 года)',
            'средняя': 'Средняя группа (4-5 лет)',
            'старшая': 'Старшая группа (5-6 лет)',
            'подготовительная': 'Подготовительная группа (6-7 лет)',
            'все': 'Все группы'
        }
        return group_map.get(self.age_group, self.age_group)