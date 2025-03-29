from app import app, db, User
from werkzeug.security import generate_password_hash

with app.app_context():
# Короче благодаря этому файлу мы можем добавлять в базу данных разных пользователей, воспользуйся Python add_admin.py в консоли
    hashed_password = generate_password_hash('student', method='pbkdf2:sha256')


    student_user = User(username='student', password=hashed_password, group='student')


    db.session.add(student_user)
    db.session.commit()

print("Пользователь admin с паролем admin добавлен в базу данных.")