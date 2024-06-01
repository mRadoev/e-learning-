from fastapi import APIRouter, Response, status, HTTPException, Header

from common.auth import get_user_or_raise_401
from data.models import User, LoginData
from services import users_services, courses_services
from services.users_services import is_authenticated, give_user_info, find_by_email, email_exists, create, create_token, try_login, find_by_id

#Initial functionality, viewing all users not mandatory, but helpful for testing purposes
users_router = APIRouter(prefix='/users')


#
@users_router.get('/')
def show_users(x_token: str = Header()):
    pass


@users_router.get('/id/{user_id}')
def show_user_by_id(user_id: int, x_token: str = Header()):
    if is_authenticated(x_token):
        user_info = give_user_info(user_id)
        if user_info:
            return user_info
        else:
            raise HTTPException(status_code=404, detail="User not found")
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")


@users_router.get('/email/{user_email}')
def show_user_by_email(user_email: str, x_token: str = Header()):
    if is_authenticated(x_token):
        user = find_by_email(user_email)
        if user:
            user_info = give_user_info(user.id)
            return user_info
        else:
            raise HTTPException(status_code=404, detail="User not found")
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")


#Guests must be able to register
#Admins could authorize teachers' registrations(via email)
@users_router.post('/register')
def registration(data: User):
    if email_exists(data.email):
        raise HTTPException(status_code=400, detail="Email already registered")

    user = create(data.role, data.first_name, data.last_name, data.password, data.email)
    if user:
        return {"message": "User registered successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to register user")


@users_router.post('/login')
def login(data: LoginData):
    user = try_login(data.email, data.password)
    if user.role == 'teacher':
        requests = courses_services.show_pending_requests(user.user_id)
    if user:
        # if login is successful, token is created
        token = create_token(user)
        if requests:
            return {"token": token}, "You have pending enrollment requests!"
        return {"token": token}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")


@users_router.post('/logout')
def logout(response: Response):
    # clear token from client's storage (e.g., local storage, session storage, cookies)
    response.delete_cookie("token")
    return {"message": "Logged out successfully"}

@users_router.put('/account')
def update_user(data: dict, x_token: str = Header()):
    user = get_user_or_raise_401(x_token)
    if data.get('user_id') or data.get('role'):
        return "You cannot change your ID or role."

    users_services.update_user(data, user.user_id)

    return "User info updated successfully!"


#Students can edit everything about their account information except their email (I assume they can't edit their id)
#Teachers can edit everything about their account information except their names (I assume they can't edit their id)

