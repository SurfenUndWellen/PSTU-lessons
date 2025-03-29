from app import app, db, User
from werkzeug.security import generate_password_hash

# Создаем контекст приложения
with app.app_context():
    # Хэшируем пароль
    hashed_password = generate_password_hash('admin', method='pbkdf2:sha256')

    # Создаем пользователя
    admin_user = User(username='admin', password=hashed_password, group='admin')

    # Добавляем пользователя в сессию и сохраняем в базе данных
    db.session.add(admin_user)
    db.session.commit()

print("Пользователь admin с паролем admin добавлен в базу данных.")