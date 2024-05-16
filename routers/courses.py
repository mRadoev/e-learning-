from fastapi import APIRouter, Response, status, HTTPException, Header, Query


category_router = APIRouter(prefix='/courses')

@category_router.get('/')
def show_courses(x_token: str = Header()):
    pass

@category_router.get('/id/{course_id}')
def show_course_by_id(course_id, x_token: str = Header()):
    pass

@category_router.get('/title/{course_title}')
def show_course_by_id(course_title, x_token: str = Header()):
    pass

