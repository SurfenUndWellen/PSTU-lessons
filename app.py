from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

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


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
@login_required
def home():
    return render_template('index.html', current_user=current_user)
@app.route('/kg')
@login_required
def kg():
    return render_template('kg.html')
@app.route('/pc')
@login_required
def pc():

    return render_template('pc.html')
@app.route('/odb')
@login_required
def odb():
    return render_template('odb.html')
@app.route('/al')
@login_required
def al():
    return render_template('al.html')
@app.route('/el')
@login_required
def el():
    return render_template('el.html')
@app.route('/student')
def student():
    if request.method == 'POST':
        name = request.form['name']
        surname = request.form['surname']
        patronymic = request.form['patronymic']
        new_student = Student(name=name, surname=surname, patronymic=patronymic)
        db.session.add(new_student)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('student.html')
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
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)