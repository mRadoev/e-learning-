from fastapi import APIRouter, status, HTTPException, Header, Depends, Request
from data.models import Course, Role, Email, CustomParams, CustomPage
from common.auth import get_user_or_raise_401
from typing import Optional
from services import courses_services
from fastapi_pagination import Page, Params, paginate
from services.users_services import decode_token
from fastapi_pagination.utils import disable_installed_extensions_check

disable_installed_extensions_check()

courses_router = APIRouter(prefix='/courses')


# Teachers can access all courses they own (only?)
# Students can only view public courses and premium courses that they have access to(CourseHasUsers table)
# Guests can only view public courses


@courses_router.get('/', response_model=CustomPage)
def show_courses(request: Request, params: CustomParams = Depends(), x_token: Optional[str] = Header(None)):
    base_url = str(request.base_url)
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

    paginated_courses = paginate(courses, params)

    # Create the custom page response
    custom_page = CustomPage.create(paginated_courses.items, paginated_courses.total, params)
    previous_int = custom_page.previous_page
    next_int = custom_page.next_page
    custom_page.previous_page = f"{base_url}courses?page={previous_int}" if previous_int else "This is the first page"
    custom_page.next_page = f"{base_url}courses?page={next_int}" if next_int else "This is the last page"

    return custom_page


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

    if user_role == 'admin':
        return check_course
    elif check_course.status == 0 and logged_user is None:
        return courses_services.by_id_for_guest(course_id)
    elif check_course.status == 0:
        return courses_services.by_id_for_non_guest(course_id)
    elif user_role == 'student' and check_course.status == 1:
        course_to_show = courses_services.by_id_for_student(user_id, course_id)
        return course_to_show
    elif user_role == 'teacher' and check_course.status == 1:
        course_to_show = courses_services.by_id_for_teacher(user_id, course_id)
        return course_to_show
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")


# Only available to logged users

@courses_router.get('/any')
def experiment(data: dict):
    course_id = data.get('course_id')
    return courses_services.grab_any_course_by_id(course_id)


@courses_router.get('/title/{course_title}')
def show_courses_by_title(course_title, x_token: str = Header(None)):
    if x_token:
        logged_user = get_user_or_raise_401(x_token)
        user_id = logged_user.user_id
        user_role = logged_user.role
    else:
        user_role = None
        user_id = None

    if user_role is None:
        courses_to_show = courses_services.by_title_for_guest(course_title)
        return courses_to_show
    if user_role == 'student':
        courses_to_show = courses_services.by_title_for_student(course_title, user_id)
        return courses_to_show
    if user_role == 'teacher':
        courses_to_show = courses_services.by_title_for_teacher(course_title, user_id)
        return courses_to_show
    elif user_role == 'admin':
        courses_to_show = courses_services.by_title_for_admin(course_title)
        return courses_to_show
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    #
    # courses = courses_services.grab_any_course_by_title(title.get('title'), user_id, user_role)
    # return courses


# Available to guests
@courses_router.get('/tag/{tag}')
def show_courses_by_tag(tag, x_token: str = Header()):
    if x_token:
        logged_user = get_user_or_raise_401(x_token)
        user_id = logged_user.user_id
        user_role = logged_user.role
    else:
        user_role = None
        user_id = None

    if user_role is None:
        courses_to_show = courses_services.by_tag_for_guest(tag)
        return courses_to_show
    if user_role == 'student':
        courses_to_show = courses_services.by_tag_for_student(tag, user_id)
        return courses_to_show
    if user_role == 'teacher':
        courses_to_show = courses_services.by_tag_for_teacher(tag, user_id)
        return courses_to_show
    if user_role == 'admin':
        courses_to_show = courses_services.by_tag_for_admin(tag)
        return courses_to_show
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")


#Will show all courses for guests and users by either ascending or descending order
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

    new_course = courses_services.create_course(course_data, user.user_id)
    return "New course created successfully!", new_course


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
        return "Course ID must be entered as a Path parameter."

    course = courses_services.grab_any_course_by_id(course_id)

    if user.role != "teacher" or course.owner_id != user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Only teachers that own the course can edit it!")

    courses_services.update_course(data, course_id)

    return "Course updated successfully!"


# (only?)Students can enroll in up to 5 premium courses and unlimited public courses
# Teachers should be able to approve enrollment requests and could be notified by email about the request
@courses_router.post("/enroll/id/{course_id}")
def enroll_in_course(course_id: int, x_token: str = Header(...)):
    user = get_user_or_raise_401(x_token)
    if user.role != "student":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only students can send enrollment requests.")

    courses_services.check_premium_limit_reached(user.user_id)
    result = courses_services.send_enrollment_request(user.user_id, course_id)
    return result


@courses_router.get("/requests")
def show_requests(x_token: str = Header(...)):
    user = get_user_or_raise_401(x_token)
    if user.role != "teacher":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only teachers can have requests.")

    emails = courses_services.show_pending_requests(user.user_id)
    if emails:
        return emails
    return "You have no pending requests!"


@courses_router.post("/requests/{response}")
def respond_request(data: Email, response: str = "approve" or "reject", x_token: str = Header(...)):
    user = get_user_or_raise_401(x_token)
    if user.role != "teacher":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only teachers can have requests.")

    if response == "approve":
        response = True
        answer = "approved"
    else:
        response = False
        answer = "rejected"

    courses_services.check_premium_limit_reached(data.sender_id)
    courses_services.respond_to_request(data.course_id, data.sender_id, response)
    emails = courses_services.show_pending_requests(user.user_id)
    return (f"Student with ID #{data.sender_id} has been {answer} for course with ID #{data.course_id}"
            " {course title}"), emails


@courses_router.post("/unsubscribe/id/{course_id}")
def unsubscribe_from_course_endpoint(course_id: int, x_token: str = Header(...)):
    user = get_user_or_raise_401(x_token)
    if user.role != "student":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only students can unsubscribe from courses.")

    result = courses_services.unsubscribe_from_course(user.user_id, course_id)
    return result


@courses_router.get("/id/{course_id}/users")
def get_users_from_course(request: Request, course_id: int, params: CustomParams = Depends(), x_token: str = Header()):
    base_url = str(request.base_url)
    user = get_user_or_raise_401(x_token)
    course = courses_services.grab_any_course_by_id(course_id)
    if user.role == "admin":
        users = courses_services.get_course_user_admin(course_id)

    elif user.role == "teacher":
        if course.owner_id != user.user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Only teachers who own the course can view its users.")
        users = courses_services.get_course_user_teacher(course_id, user.user_id)

    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Only teachers can view users in courses.")

    paginated_users = paginate(users, params)

    # Create the custom page response
    custom_page = CustomPage.create(paginated_users.items, paginated_users.total, params)
    previous_int = custom_page.previous_page
    next_int = custom_page.next_page
    custom_page.previous_page = f"{base_url}courses/id/{course_id}/users?page={previous_int}" if previous_int else "This is the first page"
    custom_page.next_page = f"{base_url}courses/id/{course_id}/users?page={next_int}" if next_int else "This is the last page"

    return custom_page


@courses_router.get("/report/id/{course_id}")
def generate_report(course_id: int, x_token: str = Header()):
    user = get_user_or_raise_401(x_token)
    course = courses_services.grab_any_course_by_id(course_id)
    if user.role != "teacher":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Only teachers can generate reports.")
    if user.user_id != course.owner_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Only teachers that own the course can generate report for it.")

    report = courses_services.generate_report(course_id)
    return report
# Students should be able to rate courses that they've enrolled in
