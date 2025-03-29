from app import app, db, Student

# Инициализация контекста приложения
with app.app_context():
    Student = Student.query.all()
    for student in Student:
        print(f"ID: {Student.id}, name: {Student.name}, surname: {Student.surname}, patronymic: {Student.patronymic}")