from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.column(db.Integer, primary_key=True)
    login = db.column(db.string(80), unique=True, nullable=False)
    password = db.column(db.string(80), unique=True, nullable=False)
    group = db.Column(db.String(25), nullable=False)
@app.route('/')
def home():
    return render_template('index.html')
@app.route('/kg')
def kg():
    return render_template('kg.html')
@app.route('/pc')
def pc():
    return render_template('pc.html')
@app.route('/odb')
def odb():
    return render_template('odb.html')
@app.route('/al')
def al():
    return render_template('al.html')
@app.route('/el')
def el():
    return render_template('el.html')
@app.route('/student')
def student():
    return render_template('student.html')
@app.route('/login')
def login():
    return render_template('login.html')
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)