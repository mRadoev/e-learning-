from data.database import insert_query, read_query, update_query
from data.models import User, Course
from typing import Optional
from mariadb import IntegrityError
from fastapi import HTTPException
import mariadb
import jwt
import bcrypt
from flask import session


def find_by_id(user_id: int) -> User | None:
    data = read_query(
        f'SELECT user_id, role, email, first_name, last_name, password FROM users WHERE user_id = {user_id}')
    return next((User.from_query_result(*row) for row in data), None)


def find_by_email(email: str) -> User | None:
    data = read_query(
        'SELECT user_id, role, email, first_name, last_name, password FROM users WHERE email = ?',
        (email,))

    return next((User.from_query_result(*row) for row in data), None)


def try_login(email: str, password: str) -> Optional[User]:
    user = find_by_email(email)
    if user and verify_password(password, user.password):
        return user
    return None


def create(role: str, first_name: str, last_name: str, password: str, email: str) -> User | None:
    hashed_password = hash_password(password)
    generated_id = insert_query(
        'INSERT INTO users(role, first_name, last_name, password, email) VALUES (?,?,?,?,?)',
        (role, first_name, last_name, hashed_password, email)
    )

    if role == 'student':
        insert_query(f'INSERT INTO students(student_id) VALUES ({generated_id})')

    if role == 'teacher':
        insert_query(f'INSERT INTO teachers(teacher_id) VALUES ({generated_id})')

    return User(user_id=generated_id, role=role, first_name=first_name, last_name=last_name, password=hashed_password,
                email=email)


def create_token(user: User) -> str:
    # Payload for the JWT token
    payload = {
        'user_id': user.user_id,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'role': user.role,
        'password': user.password
    }

    # Replace 'your_secret_key' with a secure secret key
    token = jwt.encode(payload, 'secret_key', algorithm='HS256')

    return token


def decode_token(token: str) -> dict:
    payload = jwt.decode(token, 'secret_key', algorithms=['HS256'])
    return payload


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


def find_by_id_and_email(user_id: int, email: str) -> bool:
    try:
        # Execute a SELECT query to check if the user exists
        query = "SELECT user_id FROM users WHERE user_id = ? AND email = ?"
        result = read_query(query, (user_id, email))

        return result is not None

    except mariadb.Error as error:
        print("Error:", error)
        return False


def is_authenticated(token: str) -> bool:
    try:
        payload = jwt.decode(token, 'secret_key', algorithms=['HS256'])

        user_id = payload.get('user_id')
        email = payload.get('email')

        user_exists = find_by_id_and_email(user_id, email)  # check if user exists

        return user_exists

    except jwt.ExpiredSignatureError:
        return False
    except jwt.InvalidTokenError:
        return False


def logged_in():
    return 'user_id' in session


def from_token(token: str) -> User:
    payload = decode_token(token)
    user_id = payload.get("user_id")
    first_name = payload.get("first_name")
    last_name = payload.get("last_name")
    role = payload.get("role")
    email = payload.get("email")
    password = payload.get("password")

    user = User(user_id=user_id, first_name=first_name, last_name=last_name, role=role, email=email, password=password)

    return user


def email_exists(email: str):
    data = read_query('SELECT email FROM users WHERE email = ?', (email,))
    if data:
        return True

    return False


def give_user_info(user_id: int):
    data = read_query('SELECT user_id, role, email, first_name, last_name FROM users WHERE user_id = ?', (user_id,))
    return [User.from_query_result(*row) for row in data]


def update_user(data: dict, user_id):
    for key, value in data.items():
        if type(value) is str:
            value = '"' + f'{value}' + '"'
        update_query(f'''UPDATE users
                        SET {key} = {value} 
                        WHERE user_id = {user_id}''')


def show_student_courses(user_id: int):
    data = read_query(f'''SELECT c.course_id, c.owner_id, c.title, c.description, c.objectives, c.tags, c.status 
                        FROM courses c
                        JOIN students_has_courses sc ON sc.course_id = c.course_id
                        WHERE sc.user_id = {user_id} AND sc.subscription_status = 1''')
    courses = [Course.from_query_result(*row) for row in data]
    if courses:
        return courses
    raise HTTPException(status_code=404, detail="Student not enrolled in any courses!")


def show_teacher_courses(user_id: int):
    data = read_query(f'''SELECT c.course_id, c.owner_id, c.title, c.description, c.objectives, c.tags, c.status 
                        FROM courses c
                        WHERE c.owner_id = {user_id}''')
    courses = [Course.from_query_result(*row) for row in data]
    if courses:
        return courses
    raise HTTPException(status_code=404, detail="Teacher does not own any courses!")
