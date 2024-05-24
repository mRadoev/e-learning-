from fastapi import HTTPException
from data.models import User
from services.users_services import is_authenticated, from_token


def get_user_or_raise_401(token: str) -> User:
    if not is_authenticated(token): #May not be necessary check, same check is in from_token function below in return statement
        raise HTTPException(status_code=401, detail="Unauthorized: User not authenticated!")

    return from_token(token)