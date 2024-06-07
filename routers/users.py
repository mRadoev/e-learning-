from fastapi import APIRouter, Response, HTTPException, Header, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from common.auth import get_user_or_raise_401
from data.models import User, LoginData
from services import users_services, courses_services
from services.users_services import is_authenticated, give_user_info, find_by_email, email_exists, create, create_token, try_login, find_by_id

#Initial functionality, viewing all users not mandatory, but helpful for testing purposes
users_router = APIRouter(prefix='/users')
templates = Jinja2Templates(directory="templates")


@users_router.get("/registration", response_class=HTMLResponse)
async def get_register_form(request: Request):
    return templates.TemplateResponse("users/register.html", {"request": request})

@users_router.get('/id/{user_id}', response_class=HTMLResponse)
def show_user_by_id(request: Request, user_id: int, x_token: str = Header()):
    if is_authenticated(x_token):
        user_info = give_user_info(user_id)
        return templates.TemplateResponse('users/profile.html', {"request": request, "user_info": user_info})
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")


@users_router.get('/email/{user_email}', response_class=HTMLResponse)
def show_user_by_email(request: Request, user_email: str, x_token: str = Header()):
    if is_authenticated(x_token):
        user = find_by_email(user_email)
        if user:
            user_info = give_user_info(user.user_id)
            return templates.TemplateResponse('users/profile.html', {"request": request, "user_info": user_info})
        else:
            raise HTTPException(status_code=404, detail="User not found")
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")


#Guests must be able to register
#Admins could authorize teachers' registrations(via email)
@users_router.post("/register", response_class=HTMLResponse)
async def register(request: Request):
    form = await request.form()

    role = form.get('role')
    first_name = form.get('first_name')
    last_name = form.get('last_name')
    email = form.get('email')
    password = form.get('password')

    if email_exists(email):
        raise HTTPException(status_code=400, detail="Email already registered")

    user = create(role, first_name, last_name, password, email)
    if user:
        return templates.TemplateResponse('users/registration_success.html', {"request": request})
    else:
        raise HTTPException(status_code=500, detail="Failed to register user")


@users_router.post('/login', response_class=HTMLResponse)
def login(request: Request, email: str, password: str):
    user = try_login(email, password)
    requests = None
    if user:
        if user.role == 'teacher':
            requests = courses_services.show_pending_requests(user.user_id)

        token = create_token(user)
        response = templates.TemplateResponse('users/login_success.html', {"request": request, "requests": requests})
        response.set_cookie(key="token", value=token)
        return response
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")


@users_router.post('/logout', response_class=HTMLResponse)
def logout(request: Request, response: Response):
    response = templates.TemplateResponse('users/logout_success.html', {"request": request})
    response.delete_cookie("token")
    return response

@users_router.put('/account', response_class=HTMLResponse)
def update_user(request: Request, data: dict, x_token: str = Header()):
    user = get_user_or_raise_401(x_token)
    if data.get('user_id') or data.get('role'):
        return "You cannot change your ID or role."

    users_services.update_user(data, user.user_id)
    return templates.TemplateResponse('users/account_update_success.html', {"request": request})


#Students can edit everything about their account information except their email (I assume they can't edit their id)
#Teachers can edit everything about their account information except their names (I assume they can't edit their id)

