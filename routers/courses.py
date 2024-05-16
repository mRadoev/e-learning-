from fastapi import APIRouter, Response, status, HTTPException, Header, Query
from data.models import Course


category_router = APIRouter(prefix='/courses')

#Students can only view public courses or premium courses that they have access to
#Guests can only view public courses
@category_router.get('/')
def show_courses(x_token: str = Header()):
    pass

#Only available to logged users
@category_router.get('/id/{course_id}')
def show_course_by_id(course_id, x_token: str = Header()):
    pass

#Only available to logged users
@category_router.get('/title/{course_title}')
def show_course_by_id(course_title, x_token: str = Header()):
    pass

#Available to guests
@category_router.get('/tag/{tag}')
def show_courses_by_tag(tag, x_token: str = Header()):
    pass

#Available to guests
@category_router.get('/rating/{rating}')
def show_courses_by_rating(rating, x_token: str = Header()):
    pass


#Only teachers can create new courses
@category_router.post('/new')
def create_course(data: Course, x_token: str = Header()):
    pass


@category_router.put('/update')
def update_course(data, x_token: str = Header()):
    pass

