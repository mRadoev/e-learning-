from data.database import insert_query, read_query, update_query
from data.models import User
from typing import Optional
from mariadb import IntegrityError
from fastapi import HTTPException
import mariadb
import jwt
import bcrypt
from flask import session


# _SEPARATOR = ';'

def find_by_id(user_id: int) -> User | None:
    data = read_query(
        f'SELECT user_id, role, email, first_name, last_name, password FROM users WHERE user_id = {user_id}')
    return next((User.from_query_result(*row) for row in data), None)


def find_by_email(email: str) -> User | None:
    data = read_query(
        'SELECT user_id, role, email, first_name, last_name, password FROM users WHERE email = ?',
        (email,))

    return next((User.from_query_result(*row) for row in data), None)


from typing import Optional


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

    return User(user_id=generated_id, role=role, first_name=first_name, last_name=last_name, password=hashed_password, email=email)

    # except IntegrityError:
    #     # mariadb raises this error when a constraint is violated
    #     # in that case we have duplicate emails
    #     return None


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
    #?Need to encrypt the password with token.
    #!Check if password is correct when token checks email and id
    user_exists = find_by_id_and_email(user_id, email)
    if user_exists:
        if user_id is None or role is None or email is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        return user


# def name_exists(name: str):
#     data = read_query('SELECT COUNT(*) from users WHERE username = ?', (name,))
#     if data == [(0,)]:
#         return False
#
#     return True


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


# def get_user_role_from_token(token: str) -> Optional[str]:
#     try:
#         payload = jwt.decode(token, 'secret_key', algorithms=['HS256'])
#         user_role = payload.get('role')
#         return user_role
#     except jwt.InvalidTokenError:
#         print("Invalid token")
#         return None
