from data.database import insert_query, read_query
from data.models import User
from typing import Optional
from mariadb import IntegrityError
import mariadb
import jwt
from flask import session

_SEPARATOR = ';'


# passwords should be secured as hashstrings in DB
# def _hash_password(password: str):
#     from hashlib import sha256
#     return sha256(password.encode('utf-8')).hexdigest()


def find_by_email(email: str) -> User | None:
    data = read_query(
        'SELECT user_id, role, email, first_name, last_name, password FROM users WHERE email = ?',
        (email,))

    return next((User.from_query_result(*row) for row in data), None)


def try_login(email: str, password: str) -> User | None:
    user = find_by_email(email)

    # password = _hash_password(password)
    if user.password == password:
        return user
    return None


def create(role: str, first_name: str, last_name: str, password: str, email: str) -> User | None:
    # password = _hash_password(password)
    try:
        generated_id = insert_query(
            'INSERT INTO users(role, first_name, last_name, password, email) VALUES (?,?,?,?,?)',
            (role, first_name, last_name, password, email))

        return User(id=generated_id, role=role, first_name=first_name, last_name=last_name, password=password, email=email)

    except IntegrityError:
        # mariadb raises this error when a constraint is violated
        # in that case we have duplicate emails
        return None


def create_token(user: User) -> str:
    # Payload for the JWT token
    payload = {
        'user_id': user.user_id,
        'email': user.email
    }

    # Replace 'your_secret_key' with a secure secret key
    token = jwt.encode(payload, 'secret_key', algorithm='HS256')

    return token


def decode_token(token: str) -> dict:
    payload = jwt.decode(token, 'secret_key', algorithms=['HS256'])

    return payload


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

        user_exists = find_by_id_and_email(user_id, email)

        return user_exists

    except jwt.ExpiredSignatureError:
        # token expiration error
        return False

    except jwt.InvalidTokenError:
        # invalid token error
        return False


def logged_in():
    return 'user_id' in session


def from_token(token: str) -> User | None:
    email = token.split(_SEPARATOR)

    return find_by_email(*email)


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
    data = read_query('SELECT user_id, first_name, last_name, email FROM users WHERE user_id = ?', (user_id,))

    return [User.from_query_result(*row) for row in data]


def get_user_role_from_token(token: str) -> Optional[str]:
    try:
        payload = jwt.decode(token, 'secret_key', algorithms=['HS256'])
        user_role = payload.get('role')
        return user_role
    except jwt.InvalidTokenError:
        print("Invalid token")
        return None