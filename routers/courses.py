from fastapi import APIRouter, status, HTTPException, Header, Depends, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from data.models import Course, Role, Email, CustomParams, CustomPage
from common.auth import get_user_or_raise_401
from services import courses_services, sections_services
from fastapi_pagination import paginate
from fastapi_pagination.utils import disable_installed_extensions_check

disable_installed_extensions_check()
templates = Jinja2Templates(directory="templates")
courses_router = APIRouter(prefix='/courses')


@courses_router.get('/', response_class=HTMLResponse, tags=["Courses"])  #TESTED
def show_courses(request: Request, params: CustomParams = Depends()):
    cookie_value = request.cookies.get('jwt_token')
    x_token = cookie_value
    if x_token:
        logged_user = get_user_or_raise_401(x_token)
    else:
        logged_user = None

    # Retrieve courses based on user role or guest status
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

    # Paginate courses
    paginated_courses = paginate(courses, params)

    # Create the custom page response
    custom_page = CustomPage.create(paginated_courses.items, paginated_courses.total, params)

    return templates.TemplateResponse("courses/show_courses.html",
                                      {"request": request, "courses": paginated_courses.items,
                                       "custom_page": custom_page})


@courses_router.get('/id/{course_id}', response_class=HTMLResponse, tags=["Courses"])
def show_course_details(request: Request, course_id: int):
    cookie_value = request.cookies.get('jwt_token')
    x_token = cookie_value
    logged_user = None

    if x_token:
        logged_user = get_user_or_raise_401(x_token)
        user_id = logged_user.user_id
        user_role = logged_user.role
    else:
        user_role = None
        user_id = None

    check_course = courses_services.grab_any_course_by_id(course_id)

    if user_role == 'admin':
        course_details = check_course
    elif check_course.status == 0 and logged_user is None:
        course_details = courses_services.by_id_for_guest(course_id)
    elif check_course.status == 0:
        course_details = courses_services.by_id_for_non_guest(course_id)
    elif user_role == 'student' and check_course.status == 1:
        course_details = courses_services.by_id_for_student(user_id, course_id)
    elif user_role == 'teacher' and check_course.status == 1:
        course_details = courses_services.by_id_for_teacher(user_id, course_id)

    if course_details:
        sections_to_show = sections_services.grab_sections_by_course(course_id)
        return templates.TemplateResponse("courses/course_details.html",
                                          {"request": request, "course": course_details, "sections": sections_to_show})
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")


@courses_router.get('/any', tags=["Courses"])
def experiment(data: dict):
    course_id = data.get('course_id')
    return courses_services.grab_any_course_by_id(course_id)


@courses_router.get('/title/', tags=["Courses"])  #TESTED
def show_courses_by_title(request: Request, search: str = None):
    cookie_value = request.cookies.get('jwt_token')
    x_token = cookie_value
    if x_token:
        logged_user = get_user_or_raise_401(x_token)
        user_id = logged_user.user_id
        user_role = logged_user.role
    else:
        user_role = None
        user_id = None

    course_title = None
    courses_to_show = None

    if search:
        course_title = search
        if user_role is None:
            courses_to_show = courses_services.by_title_for_guest(course_title)
        elif user_role == 'student':
            courses_to_show = courses_services.by_title_for_student(course_title, user_id)
        elif user_role == 'teacher':
            courses_to_show = courses_services.by_title_for_teacher(course_title, user_id)
        elif user_role == 'admin':
            courses_to_show = courses_services.by_title_for_admin(course_title)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")

    return templates.TemplateResponse("courses/courses_by_title.html",
                                      {"request": request, "course_title": course_title, "courses": courses_to_show})


@courses_router.get('/tag', tags=["Courses"])  #To be implemented!
def show_courses_by_tag(request: Request, search: str = None, x_token: str = Header(None)):
    if x_token:
        logged_user = get_user_or_raise_401(x_token)
        user_id = logged_user.user_id
        user_role = logged_user.role
    else:
        user_role = None
        user_id = None

    tag = None
    courses_to_show = None

    if search:
        tag = search
        if user_role is None:
            courses_to_show = courses_services.by_tag_for_guest(tag)
        elif user_role == 'student':
            courses_to_show = courses_services.by_tag_for_student(tag, user_id)
        elif user_role == 'teacher':
            courses_to_show = courses_services.by_tag_for_teacher(tag, user_id)
        elif user_role == 'admin':
            courses_to_show = courses_services.by_tag_for_admin(tag)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")

    return templates.TemplateResponse("courses/courses_by_tag.html",
                                      {"request": request, "tag": tag, "courses": courses_to_show})


@courses_router.get('/rating/{rating}', tags=["Courses"])
def show_courses_by_rating(rating, x_token: str = Header()):
    pass


@courses_router.get("/create_form", response_class=HTMLResponse, tags=["Courses"])  #TESTED
async def get_course_form(request: Request):
    return templates.TemplateResponse("courses/create_course.html", {"request": request})


@courses_router.post('/create', response_class=HTMLResponse, tags=["Courses"])
async def create_course(request: Request, course_data: Course = None):
    if course_data:  # If course_data is provided as JSON data
        title = course_data.title
        description = course_data.description
        objectives = course_data.objectives
        tags = course_data.tags
        status = course_data.status
    else:  # If form data is provided
        form = await request.form()
        title = form.get('title')
        description = form.get('description')
        objectives = form.get('objectives')
        tags = form.get('tags')
        status = form.get('status')

    if not all([title, description, objectives]):
        raise HTTPException(status_code=422, detail="Missing required fields")

    try:
        status = int(status)
    except ValueError:
        raise HTTPException(status_code=422, detail="Invalid status value")

    x_token = request.cookies.get("jwt_token")
    if not x_token:
        raise HTTPException(status_code=401, detail="You need to log in first!")

    user = get_user_or_raise_401(x_token)
    if user.role != "teacher":
        raise HTTPException(status_code=403, detail="Only teachers can create courses")

    course_data = Course(
        title=title,
        description=description,
        objectives=objectives,
        tags=tags,
        status=int(status)
    )

    new_course = courses_services.create_course(course_data, user.user_id)

    return templates.TemplateResponse('courses/create_course_success.html', {"request": request, "course": new_course})


########To optimize and fix
# @courses_router.delete('/delete')
# def delete_course(data, x_token: str = Header()):
#     # user = get_user_or_raise_401(x_token)
#     # if user.role == "admin":
#     #     pass
#     # if user.role == "teacher":
#     #     pass
#     if data.course_id:
#         course_id = data.course_id
#     result = courses_services.delete_course(data.course_id, data.title, x_token)
#     return result


# Admins can remove access to courses for students(CourseHasUsers)
# Students must be able to unsubscribe from premium courses
@courses_router.put('/update/id/{course_id}', tags=["Courses"])
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


@courses_router.get("/enrollment_form", response_class=HTMLResponse, tags=["Courses"])  #TESTED
async def get_enrollment_form(request: Request):
    return templates.TemplateResponse("courses/enrollment_form.html", {"request": request})


# @courses_router.post("/enroll/id/{course_id}")  #Make it to title, searching for title in enrollment form
# def enroll_in_course(request: Request, course_id: int):
#     cookie_value = request.cookies.get('jwt_token')
#     x_token = cookie_value
#     user = get_user_or_raise_401(x_token)
#     if user.role != "student":
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only students can send enrollment requests.")
#
#     courses_services.check_premium_limit_reached(user.user_id)
#     result = courses_services.send_enrollment_request(user.user_id, course_id)
#     return result

@courses_router.post("/enroll/id/{course_id}", tags=["swagger_presentation"])
def enroll_in_course(course_id: int, x_token: str = Header(...)):
    user = get_user_or_raise_401(x_token)
    if user.role != "student":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only students can send enrollment requests.")

    courses_services.check_premium_limit_reached(user.user_id)
    result = courses_services.send_enrollment_request(user.user_id, course_id)
    return result


@courses_router.get("/requests", tags=["swagger_presentation"])
def show_requests(x_token: str = Header(...)):
    user = get_user_or_raise_401(x_token)
    if user.role != "teacher":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only teachers can have requests.")

    emails = courses_services.show_pending_requests(user.user_id)
    if emails:
        return emails
    return "You have no pending requests!"


@courses_router.post("/requests/{response}", tags=["swagger_presentation"])
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
    request_answered = courses_services.respond_to_request(data.course_id, data.sender_id, response)
    #Check which exception is more appropriate
    if request_answered:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Student has already been approved")

    emails = courses_services.show_pending_requests(user.user_id)
    if emails:
        return (f"Student with ID #{data.sender_id} has been {answer} for course with ID #{data.course_id}"
                " {course title}"), emails
    return (f"Student with ID #{data.sender_id} has been {answer} for course with ID #{data.course_id}"
            " {course title}")


@courses_router.post("/unsubscribe/id/{course_id}", tags=["Courses"])  #Make by title
def unsubscribe_from_course_endpoint(course_id: int, x_token: str = Header(...)):
    user = get_user_or_raise_401(x_token)
    if user.role != "student":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only students can unsubscribe from courses.")

    result = courses_services.unsubscribe_from_course(user.user_id, course_id)
    return result


@courses_router.get("/id/{course_id}/users", response_class=HTMLResponse, tags=["Courses"])
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
    custom_page = CustomPage.create(paginated_users.items, paginated_users.total, params)

    previous_int = custom_page.previous_page
    next_int = custom_page.next_page
    previous_page = f"{base_url}courses/id/{course_id}/users?page={previous_int}" if previous_int else "This is the first page"
    next_page = f"{base_url}courses/id/{course_id}/users?page={next_int}" if next_int else "This is the last page"

    return templates.TemplateResponse("courses/course_users.html", {
        "request": request,
        "course_id": course_id,
        "users": paginated_users.items,
        "previous_page": previous_page,
        "next_page": next_page,
    })


@courses_router.get("/report/id/{course_id}", tags=["Courses"])
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
