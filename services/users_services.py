from data.database import insert_query, read_query
from data.models import User
from mariadb import IntegrityError
import mariadb
import jwt
from flask import session

_SEPARATOR = ';'


# passwords should be secured as hashstrings in DB
# def _hash_password(password: str):
#     from hashlib import sha256
#     return sha256(password.encode('utf-8')).hexdigest()


def find_by_username(username: str) -> User | None:
    data = read_query(
        'SELECT id, username, password, email FROM users WHERE username = ?',
        (username,))

    return next((User.from_query_result(*row) for row in data), None)


def try_login(username: str, password: str) -> User | None:
    user = find_by_username(username)

    # password = _hash_password(password)
    return user if user and user.password == password else None


def create(username: str, password: str, email: str) -> User | None:
    # password = _hash_password(password)
    try:
        generated_id = insert_query(
            'INSERT INTO users(username, password, email) VALUES (?,?,?)',
            (username, password, email))

        return User(id=generated_id, username=username, password='', email=email)

    except IntegrityError:
        # mariadb raises this error when a constraint is violated
        # in that case we have duplicate usernames
        return None


def create_token(user: User) -> str:
    # Define the payload for the JWT token
    payload = {
        'id': user.id,
        'username': user.username
    }

    # Note: Replace 'your_secret_key' with a secure secret key
    token = jwt.encode(payload, 'secret_key', algorithm='HS256')

    return token.encode('utf-8')


def decode_token(token: str) -> dict:
    payload = jwt.decode(token, 'secret_key', algorithms=['HS256'])

    return payload


def find_by_id_and_username(user_id: int, username: str) -> bool:
    try:
        # Execute a SELECT query to check if the user exists
        query = "SELECT id FROM users WHERE id = ? AND username = ?"
        result = read_query(query, (user_id, username))

        return result is not None

    except mariadb.Error as error:
        print("Error:", error)
        return False


def is_authenticated(token: str) -> bool:
    try:
        payload = jwt.decode(token, 'secret_key', algorithms=['HS256'])

        user_id = payload.get('id')
        username = payload.get('username')

        user_exists = find_by_id_and_username(user_id, username, )

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
    username = token.split(_SEPARATOR)

    return find_by_username(*username)


def name_exists(name: str):
    data = read_query('SELECT COUNT(*) from users WHERE username = ?', (name,))
    if data == [(0,)]:
        return False

    return True


def email_exists(email: str):
    data = read_query('SELECT COUNT(*) from users WHERE email = ?', (email,))
    if data == [(0,)]:
        return False

    return True


def give_user_info(user_id: int):
    data = read_query('SELECT id, username, password, email FROM users WHERE id = ?', (user_id,))

    return [User.from_query_result(*row) for row in data]