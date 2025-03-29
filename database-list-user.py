from app import app, db, User

# Инициализация контекста приложения
with app.app_context():
    User = User.query.all()
    for User in User:
        print(f"ID: {User.id}, username: {User.username}, password: {User.password}, group: {User.group}")