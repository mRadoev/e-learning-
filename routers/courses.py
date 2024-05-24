from fastapi import APIRouter, status, HTTPException, Header
from data.models import Course, Role
from common.auth import get_user_or_raise_401
from typing import Optional
from services import courses_services
from services.users_services import decode_token, get_user_role_from_token


courses_router = APIRouter(prefix='/courses')

# Teachers can access all courses they own (only?)
# Students can only view public courses and premium courses that they have access to(CourseHasUsers table)
# Guests can only view public courses


@courses_router.get('/')
def show_courses(x_token: Optional[str] = Header(None)):
    if x_token:
        logged_user = get_user_or_raise_401(x_token)
    else:
        logged_user = None

    # logged_user.role = get_user_role_from_token(x_token)

    # all public courses and the courses which the logged user has access to
    if not logged_user:
        courses = courses_services.guest_view()
    elif logged_user.role == Role.STUDENT:
        courses = courses_services.student_view(logged_user.user_id)
    elif logged_user.role == Role.ADMIN:
        courses = courses_services.admin_view(logged_user.user_id)
    elif logged_user.role == Role.TEACHER:
        courses = courses_services.teacher_view(logged_user.user_id)
    else:
        return "There are no courses you can view!"

    return courses


# Only available to logged users
@courses_router.get('/id/{course_id}')
def get_course_by_id(course_id: int, x_token: str = Header(None)):
    # Decode the token
    user = get_user_or_raise_401(x_token)
    user_id = user.user_id
    user_role = user.role

    course = courses_services.show_course_by_id(course_id, user_role, user_id)
    return course

# Only available to logged users
# BY TITLE may be not necessary?
# @courses_router.get('/title/{course_title}')
# def show_course_by_title(course_title: str, x_token: str = Header(...)) -> Course:
#     pass

@courses_router.get('/any')
def experiment(data: dict):
    course_id = data.get('course_id')
    return courses_services.grab_any_course_by_id(course_id)

# Available to guests
@courses_router.get('/tag/{tag}')
def show_courses_by_tag(tag, x_token: str = Header()):
    pass


# Available to guests
@courses_router.get('/rating/{rating}')
def show_courses_by_rating(rating, x_token: str = Header()):
    pass


# Only teachers can create new courses
@courses_router.post('/create')
def create_course(course_data: Course, x_token: str = Header(None)):
    if x_token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You need to log in first!")
    user = decode_token(x_token)
    # user_id = courses_services.find_sender_id(x_token)
    user_id = user.get('id')
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token or user not found")
######### May be optimized
    user_role = user.get('role')
    #user_role = courses_services.get_user_role_from_token(x_token)
    if user_role != "teacher":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only teachers can create courses")
    new_course = courses_services.create_course(course_data)
    return new_course


########To optimize and fix
@courses_router.delete('/delete')
def delete_course(data, x_token: str = Header()):
    # user = get_user_or_raise_401(x_token)
    # if user.role == "admin":
    #     pass
    # if user.role == "teacher":
    #     pass
    if data.course_id:
        course_id = data.course_id
    result = courses_services.delete_course(data.course_id, data.title, x_token)
    return result


# Teachers can only update courses that they own
# Admins can remove access to courses for students(CourseHasUsers)
# Students must be able to unsubscribe from premium courses
@courses_router.put('/update')
def update_course(data, x_token: str = Header()):
    pass


# (only?)Students can enroll in up to 5 premium courses and unlimited public courses
# Teachers should be able to approve enrollment requests and could be notified by email about the request
@courses_router.post('/enroll')
def enroll_into_course(course_id: int = None, title: str = None, x_token: str = Header()):
    pass


# Students should be able to rate courses that they've enrolled in

