from fastapi import APIRouter, Response, status, HTTPException, Header, Query

users_router = APIRouter(prefix='/sections')


@users_router.get('/')
def show_users(x_token: str = Header()):
    pass


@users_router.get('/id/{section_id}')
def show_user_by_id(section_id, x_token: str = Header()):
    pass


@users_router.get('/email/{user_email}')
def show_user_by_email(user_email, x_token: str = Header()):
    pass