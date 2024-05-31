from fastapi import APIRouter, status, HTTPException, Header
from data.models import Course, Role
from common.auth import get_user_or_raise_401
from typing import Optional
from services import courses_services
from services.users_services import decode_token


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

    # all public courses and the courses which the logged user has access to
    if not logged_user:
        courses = courses_services.guest_view()
    elif logged_user.role == Role.STUDENT:
        courses = courses_services.student_view(logged_user.user_id)
    elif logged_user.role == Role.ADMIN:
        courses = courses_services.admin_view()
    elif logged_user.role == Role.TEACHER:
        courses = courses_services.teacher_view(logged_user.user_id)
    else:
        return "There are no courses you can view!"

    return courses

#TO DO FIX CODE!!!
# Only available to logged users
@courses_router.get('/id/{course_id}')
def get_course_by_id(course_id: int, x_token: str = Header(None)):
    # Decode the token
    if x_token:
        logged_user = get_user_or_raise_401(x_token)
        user_id = logged_user.user_id
        user_role = logged_user.role
    else:
        logged_user = None

    check_course = courses_services.grab_any_course_by_id(course_id)

    if check_course.status == 0 and logged_user is None:
        #user_role = guest when no user is logged in
        return courses_services.by_id_for_guest(course_id)
    elif check_course.status == 0:
        return courses_services.by_id_for_non_guest(course_id)
    elif user_role == 'student' and check_course.status == 1:
        course_to_show = courses_services.by_id_for_student(user_id, course_id)
        return course_to_show
    elif user_role == 'teacher' and check_course.status == 1:
        course_to_show = courses_services.by_id_for_teacher(user_id, course_id)
        return course_to_show
    elif user_role == 'admin':
        return check_course
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")


# Only available to logged users

@courses_router.get('/any')
def experiment(data: dict):
    course_id = data.get('course_id')
    return courses_services.grab_any_course_by_id(course_id)


@courses_router.get('/title')
def show_courses_by_title(title, x_token: str = Header()):
    pass


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
    user = get_user_or_raise_401(x_token)
    if user.role != "teacher":
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


# Admins can remove access to courses for students(CourseHasUsers)
# Students must be able to unsubscribe from premium courses
@courses_router.put('/update/id/{course_id}')
def update_course(data: dict, course_id: int, x_token: str = Header()):
    user = get_user_or_raise_401(x_token)
    if data.get('course_id'):
        return "Course id must be entered as a Path parameter."

    course = courses_services.grab_any_course_by_id(course_id)

    if user.role != "teacher" or course.owner_id != user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only teachers that own the course can edit it!")

    courses_services.update_course(data, course_id)

    return "Course updated successfully!"



# (only?)Students can enroll in up to 5 premium courses and unlimited public courses
# Teachers should be able to approve enrollment requests and could be notified by email about the request
@courses_router.post("/enroll/id/{course_id}")
def enroll_in_course(course_id: int, x_token: str = Header(...)):
    user = get_user_or_raise_401(x_token)
    if user.role != "student":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only students can send enrollment requests.")

    result = courses_services.send_enrollment_request(user.user_id, course_id)
    return result


@courses_router.post("/unsubscribe/id/{course_id}")
def unsubscribe_from_course_endpoint(course_id: int, x_token: str = Header(...)):
    user = get_user_or_raise_401(x_token)
    if user.role != "student":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only students can unsubscribe from courses.")

    result = courses_services.unsubscribe_from_course(user.user_id, course_id)
    return result


# Students should be able to rate courses that they've enrolled in

