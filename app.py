from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
from datetime import datetime

from config import Config
from models import db, User, Material, PageVisit
from forms import LoginForm, MaterialForm

app = Flask(__name__)
app.config.from_object(Config)


db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Пожалуйста, войдите для доступа к этой странице.'


os.makedirs('static/uploads', exist_ok=True)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def create_admin():
    with app.app_context():
        admin_user = User.query.filter_by(username='admin').first()
        if not admin_user:
            admin = User(
                username='admin',
                email='admin@example.com',
                password=generate_password_hash('admin123'),
                is_admin=True
            )
            db.session.add(admin)
            db.session.commit()
            print("=== АДМИНИСТРАТОР СОЗДАН ===")
            print("Логин: admin")
            print("Пароль: admin123")
            print("===========================")
        else:
            print("=== АДМИНИСТРАТОР УЖЕ СУЩЕСТВУЕТ ===")
        
        add_initial_data()

def add_initial_data():
    
    initial_materials = [
        {
            'title': 'Мой подход: Как развивать музыкальность у детей 3-4 лет',
            'content': '''<div class="author-note">
                <strong>Автор:</strong> Парфирова Елена Юрьевна, музыкальный руководитель высшей категории
            </div>
            
            <h3>Авторская методика развития музыкальности в младшем дошкольном возрасте</h3>
            
            <p>За 15 лет работы я разработала эффективную систему развития музыкальных способностей у детей младшего дошкольного возраста. Делюсь своими наработками:</p>
            
            <h4>1. Авторские музыкальные игры</h4>
            <p>В своей практике я использую специально разработанные игры:</p>
            <ul>
                <li><strong>"Музыкальные ладошки"</strong> - развитие ритмического чувства через хлопки</li>
                <li><strong>"Звуковые дорожки"</strong> - движение под музыку с изменением темпа</li>
                <li><strong>"Волшебный мешочек"</strong> - определение инструментов по звуку</li>
            </ul>
            
            <h4>2. Проверенный репертуар</h4>
            <p>На основе многолетнего опыта я составила оптимальный список песен для этого возраста:</p>
            <ul>
                <li>"Антошка" - для развития ритма</li>
                <li>"Во саду ли, в огороде" - для координации движений</li>
                <li>"Дождик" - для развития звуковысотного слуха</li>
            </ul>''',
            'category': 'consultation',
            'target_audience': 'parents'
        },
        
        {
            'title': 'Мой опыт: Роль музыки в развитии речи дошкольников',
            'content': '''<div class="author-note">
                <strong>Автор:</strong> Парфирова Елена Юрьевна
            </div>
            
            <h3>Авторские наработки по развитию речи через музыку</h3>
            
            <p>В своей работе я активно использую музыку для коррекции речевых нарушений. Вот мои проверенные методики:</p>
            
            <h4>Авторские упражнения</h4>
            <ul>
                <li><strong>"Речевые распевки"</strong> - специально разработанные вокальные упражнения</li>
                <li><strong>"Ритмические скороговорки"</strong> - сочетание речи и ритма</li>
                <li><strong>"Звуковая гимнастика"</strong> - артикуляционные упражнения под музыку</li>
            </ul>''',
            'category': 'consultation',
            'target_audience': 'parents'
        },

        {
            'title': 'Авторский сценарий "Осенняя сказка" для средней группы',
            'content': '''<div class="author-note">
                <strong>Авторская разработка:</strong> Парфирова Елена Юрьевна
            </div>
            
            <h3>Сценарий осеннего утренника "Осенняя сказка"</h3>
            
            <h4>Музыкальный репертуар (авторская подборка):</h4>
            <ul>
                <li>Вход: "Осенний марш" (аранжировка Парфировой Е.Ю.)</li>
                <li>Песня: "Золотая осень" (обработка народной мелодии)</li>
                <li>Танец: "Листопад" (хореография Парфировой Е.Ю.)</li>
            </ul>''',
            'category': 'scenario',
            'target_audience': 'teachers'
        },

        {
            'title': 'Новогодний утренник "Волшебная снежинка" для старшей группы',
            'content': '''<div class="author-note">
                <strong>Автор:</strong> Парфирова Елена Юрьевна
            </div>
            
            <h3>Новогоднее приключение для детей 5-6 лет</h3>
            
            <h4>Музыкальные номера:</h4>
            <ul>
                <li>Песня "Маленькой елочке"</li>
                <li>Танец снежинок</li>
                <li>Хоровод "В лесу родилась елочка"</li>
            </ul>''',
            'category': 'scenario',
            'target_audience': 'teachers'
        },

        {
            'title': 'Авторская программа "Музыкальная радуга" для детей 4-5 лет',
            'content': '''<div class="author-note">
                <strong>Автор:</strong> Парфирова Елена Юрьевна
            </div>
            
            <h3>Авторская образовательная программа "Музыкальная радуга"</h3>
            
            <h4>Цель программы:</h4>
            <p>Всестороннее музыкальное развитие детей средней группы через систему интегрированных занятий.</p>
            
            <h4>Особенности программы:</h4>
            <ul>
                <li>Блочно-модульная система</li>
                <li>Интеграция с другими образовательными областями</li>
                <li>Использование ИКТ технологий</li>
            </ul>''',
            'category': 'methodical',
            'target_audience': 'teachers'
        }
    ]
    
    for material_data in initial_materials:
        existing_material = Material.query.filter_by(title=material_data['title']).first()
        if not existing_material:
            material = Material(
                title=material_data['title'],
                content=material_data['content'],
                category=material_data['category'],
                target_audience=material_data['target_audience']
            )
            db.session.add(material)
    
    db.session.commit()
    print("Начальные материалы добавлены в базу данных!")

def log_visit(page):
    visit = PageVisit(
        page=page,
        ip_address=request.remote_addr
    )
    db.session.add(visit)
    db.session.commit()

@app.route('/')
def index():
    log_visit('index')
    
    latest_materials = Material.query.filter_by(is_published=True)\
        .order_by(Material.created_date.desc())\
        .limit(6)\
        .all()
    
    stats = {
        'total_materials': Material.query.filter_by(is_published=True).count()
    }
    
    return render_template('index.html', 
                         latest_materials=latest_materials,
                         stats=stats)

@app.route('/materials')
def materials():
    log_visit('materials')
    
    category = request.args.get('category', 'all')
    audience = request.args.get('audience', 'all')
    
    query = Material.query.filter_by(is_published=True)
    
    if category != 'all':
        query = query.filter_by(category=category)
    
    if audience != 'all':
        query = query.filter_by(target_audience=audience)
    
    materials_list = query.order_by(Material.created_date.desc()).all()
    
    return render_template('materials.html', 
                         materials=materials_list,
                         current_category=category,
                         current_audience=audience)

@app.route('/material/<int:material_id>')
def material_detail(material_id):
    material = Material.query.get_or_404(material_id)
    log_visit(f'material_{material_id}')
    return render_template('material_detail.html', material=material)

@app.route('/about')
def about():
    log_visit('about')
    return render_template('about.html')

@app.route('/contacts')
def contacts():
    log_visit('contacts')
    return render_template('contacts.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin_dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('admin_dashboard'))
        else:
            flash('Неверный логин или пароль', 'error')
    
    return render_template('admin/login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/admin')
@login_required
def admin_dashboard():
    stats = {
        'total_materials': Material.query.count(),
        'published_materials': Material.query.filter_by(is_published=True).count(),
        'total_visits': PageVisit.query.count(),
        'recent_visits': PageVisit.query.filter(
            PageVisit.visit_date >= datetime.utcnow().date()
        ).count()
    }
    
    recent_materials = Material.query.order_by(Material.created_date.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html', stats=stats, recent_materials=recent_materials)

@app.route('/admin/materials', methods=['GET', 'POST'])
@login_required
def admin_materials():
    form = MaterialForm()
    
    if form.validate_on_submit():
        filename = None
        if form.file.data:
            filename = secure_filename(form.file.data.filename)
            form.file.data.save(os.path.join('static/uploads', filename))
        
        material = Material(
            title=form.title.data,
            content=form.content.data,
            category=form.category.data,
            target_audience=form.target_audience.data,
            file_path=filename
        )
        
        db.session.add(material)
        db.session.commit()
        flash('Материал успешно добавлен!', 'success')
        return redirect(url_for('admin_materials'))
    
    materials_list = Material.query.order_by(Material.created_date.desc()).all()
    return render_template('admin/materials.html', form=form, materials=materials_list)

@app.route('/admin/material/<int:material_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_material(material_id):
    material = Material.query.get_or_404(material_id)
    form = MaterialForm()
    
    if form.validate_on_submit():
        material.title = form.title.data
        material.content = form.content.data
        material.category = form.category.data
        material.target_audience = form.target_audience.data
        
        if form.file.data:
            filename = secure_filename(form.file.data.filename)
            form.file.data.save(os.path.join('static/uploads', filename))
            material.file_path = filename
        
        db.session.commit()
        flash('Материал успешно обновлен!', 'success')
        return redirect(url_for('admin_materials'))
    
    elif request.method == 'GET':
        form.title.data = material.title
        form.content.data = material.content
        form.category.data = material.category
        form.target_audience.data = material.target_audience
    
    return render_template('admin/edit_material.html', form=form, material=material)

@app.route('/admin/material/<int:material_id>/delete')
@login_required
def delete_material(material_id):
    material = Material.query.get_or_404(material_id)
    db.session.delete(material)
    db.session.commit()
    flash('Материал успешно удален!', 'success')
    return redirect(url_for('admin_materials'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory('static/uploads', filename)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        create_admin()
    app.run(debug=True)