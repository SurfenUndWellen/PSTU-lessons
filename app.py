from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Numeric
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Модели данных
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=True, nullable=False)
    group = db.Column(db.String(80), nullable=False)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    patronymic = db.Column(db.String(50), nullable=True)

class Grades(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    grade = db.Column(db.Float, nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    subject = db.Column(db.String(50), nullable=False)

# Функции аутентификации и регистрации
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Неверный логин или пароль')
    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/student', methods=['GET', 'POST'])
def student():
    if request.method == 'POST':
        name = request.form['name']
        surname = request.form['surname']
        patronymic = request.form['patronymic']
        new_student = Student(name=name, surname=surname, patronymic=patronymic)
        db.session.add(new_student)
        db.session.commit()
        return redirect(url_for('student_table'))
    return render_template('student.html')

@app.route('/student_table')
@login_required
def student_table():
    students = Student.query.all()
    return render_template('students_table.html', students_list=students)

# Функции работы с оценками и предметами
def get_subject_data(subject_name):
    students = Student.query.all()
    grades = {}
    for grade in Grades.query.filter_by(subject=subject_name.lower()).all():
        grades[grade.student_id] = grade.grade
    return {
        'students_list': students,
        'grades': grades,
        'current_subject': subject_name
    }

@app.route('/')
@login_required
def home():
    return render_template('index.html', current_user=current_user)

@app.route('/al')
@login_required
def al():
    data = get_subject_data('Алгоритмы')
    return render_template('al.html', **data)

@app.route('/kg')
@login_required
def kg():
    data = get_subject_data('Компьютерная графика')
    return render_template('kg.html', **data)

@app.route('/pc')
@login_required
def pc():
    data = get_subject_data('Физическая культура')
    return render_template('pc.html', **data)

@app.route('/odb')
@login_required
def odb():
    data = get_subject_data('Базы данных')
    return render_template('odb.html', **data)

@app.route('/el')
@login_required
def el():
    data = get_subject_data('Английский язык')
    return render_template('el.html', **data)

@app.route('/manya')
def manya():
    return render_template('index.html')

@app.route('/save_grade', methods=['POST'])
@login_required
def save_grade():
    student_id = request.form['student_id']
    subject = request.form['subject'].lower()
    grade = float(request.form['grade'])

    existing_grade = Grades.query.filter_by(
        student_id=student_id,
        subject=subject
    ).first()

    if existing_grade:
        existing_grade.grade = grade
    else:
        new_grade = Grades(
            student_id=student_id,
            subject=subject,
            grade=grade
        )
        db.session.add(new_grade)

    db.session.commit()
    
    redirect_map = {
        'алгоритмы': 'al',
        'компьютерная графика': 'kg',
        'физическая культура': 'pc',
        'базы данных': 'odb',
        'английский язык': 'el'
    }
    return redirect(url_for(redirect_map.get(subject, 'home')))

# Инициализация БД
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)