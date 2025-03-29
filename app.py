from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


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

if __name__ == '__main__':
    app.run(debug=True)