from fastapi import APIRouter, Response, status, HTTPException, Header, Query
from data.models import Course, Role
from common.auth import get_user_or_raise_401
from services import courses_services


category_router = APIRouter(prefix='/courses')

#Teachers can access all courses they own (only?)
#Students can only view public courses and premium courses that they have access to(CourseHasUsers table)
#Guests can only view public courses
@category_router.get('/')
def show_courses(x_token: str = Header()):
    #Check if there is a logged user
    if x_token:
        logged_user = get_user_or_raise_401(x_token)
    else:
        logged_user = None

    #Return all public courses and the courses which the logged user has access to
    if not logged_user:
        courses = courses_services.guest_view()
        return courses
    elif logged_user.role == Role.STUDENT:
        courses = courses_services.student_view(logged_user.user_id)
        return courses
    elif logged_user.role == Role.ADMIN:
        courses = courses_services.admin_view(logged_user.user_id)
        return courses
    elif logged_user.role == Role.TEACHER:
        courses = courses_services.teacher_view(logged_user.user_id)
        return courses



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


#Teachers can only update courses that they own
#Admins can remove access to courses for students(CourseHasUsers)
#Students must be able to unsubscribe from premium courses
@category_router.put('/update')
def update_course(data, x_token: str = Header()):
    pass


#(only?)Students can enroll in up to 5 premium courses and unlimited public courses
#Teachers should be able to approve enrollment requests and could be notified by email about the request
@category_router.post('/enroll')
def enroll_into_course(course_id: int = None, title: str = None, x_token: str = Header()):
    pass


#Courses can be deleted by admins or teachers that own them
@category_router.delete('/')
def delete_course(course_id: int = None, title: str = None, x_token: str = Header()):
    pass


#Students should be able to rate courses that they've enrolled in

