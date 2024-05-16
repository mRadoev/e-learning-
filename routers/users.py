from fastapi import APIRouter, Response, status, HTTPException, Header, Query
from data.models import User, LoginData

#Initial functionality, viewing all users not mandatory, but helpful for testing purposes
users_router = APIRouter(prefix='/users')

#
@users_router.get('/')
def show_users(x_token: str = Header()):
    pass


@users_router.get('/id/{user_id}')
def show_user_by_id(user_id, x_token: str = Header()):
    pass


@users_router.get('/email/{user_email}')
def show_user_by_email(user_email, x_token: str = Header()):
    pass

#Guests must be able to register
@users_router.post('/register')
def registration(data: User):
    pass


@users_router.post('/login')
def registration(data: LoginData):
    pass


@users_router.post('/logout')
def registration(x_token: str = Header()):
    pass