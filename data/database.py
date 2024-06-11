import os

from mariadb import connect
from mariadb.connections import Connection


def _get_connection() -> Connection:
    return connect(
        user=os.environ['E_LEARNING_DATABASE_USER'],
        password=os.environ['E_LEARNING_DATABASE_PASSWORD'],
        host=os.environ['E_LEARNING_DATABASE_HOST'],
        port=int(os.environ['E_LEARNING_DATABASE_PORT']),
        database=os.environ['E_LEARNING_DATABASE_NAME']
    )


def read_query(sql: str, sql_params=()):
    with _get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, sql_params)

        return list(cursor)


def insert_query(sql: str, sql_params=()) -> int:
    with _get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, sql_params)
        conn.commit()

        return cursor.lastrowid


def update_query(sql: str, sql_params=()) -> bool:
    with _get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, sql_params)
        conn.commit()

        return cursor.rowcount


def delete_query(sql: str, sql_params=()) -> bool:
    with _get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, sql_params)
        conn.commit()

        return True
