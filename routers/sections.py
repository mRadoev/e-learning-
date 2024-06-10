from fastapi import APIRouter, Response, status, HTTPException, Header, Depends, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from data.models import Section, Course, Role, CustomParams, CustomPage
from common.auth import get_user_or_raise_401
from services import sections_services
from fastapi_pagination import Page, Params, paginate
from typing import Optional
from services import courses_services

sections_router = APIRouter(prefix='/sections')
templates = Jinja2Templates(directory="templates")


#Teachers can access all sections they own (only?)
#Students can only view sections that are from public courses or premium courses that they have access to
#Guests cannot view sections
#Pagination for sorting sections by id or name TO DO !!!
#Remove content from shown topic parameters, show only when looking for specific topic(submenu)
@sections_router.get('/')           #TESTED
def show_sections(request: Request):
    cookie_value = request.cookies.get('jwt_token')
    x_token = cookie_value
    if x_token:
        logged_user = get_user_or_raise_401(x_token)
    else:
        logged_user = None

    if not logged_user:
        courses = sections_services.guest_view()
    elif logged_user.role == Role.STUDENT:
        courses = sections_services.student_view(logged_user.user_id)
    elif logged_user.role == Role.ADMIN:
        courses = sections_services.admin_view()
    elif logged_user.role == Role.TEACHER:
        courses = sections_services.teacher_view(logged_user.user_id)
    else:
        return "There are no courses you can view!"

    return templates.TemplateResponse('sections/show_sections.html', {"request": request})


#Content can be made not visible, because it's supposed to be long text, so instead by searching
#for the section by id or name you can view the full content of the section.
@sections_router.get('/id/{section_id}')
def show_section_by_id(section_id, x_token: str = Header()):
    pass


@sections_router.get('/title/{section_title}', response_model=CustomPage)       #TO DO
def show_section_by_title(
    section_title: str,
    request: Request,
    params: CustomParams = Depends(),
    x_token: Optional[str] = Header(None)
):
    base_url = str(request.base_url)
    user_role = None
    user_id = None

    if x_token:
        logged_user = get_user_or_raise_401(x_token)
        user_id = logged_user.user_id
        user_role = logged_user.role

    if user_role is None:
        sections_to_show = sections_services.by_title_for_guest(section_title)
    elif user_role == 'student':
        sections_to_show = sections_services.by_title_for_student(section_title, user_id)
    elif user_role == 'teacher':
        sections_to_show = sections_services.by_title_for_teacher(section_title, user_id)
    elif user_role == 'admin':
        sections_to_show = sections_services.by_title_for_admin(section_title)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")

    paginated_sections = paginate(sections_to_show, params)

    # Create the custom page response
    custom_page = CustomPage.create(paginated_sections.items, paginated_sections.total, params)
    previous_int = custom_page.previous_page
    next_int = custom_page.next_page
    custom_page.previous_page = f"{base_url}sections/title/{section_title}?page={previous_int}" if previous_int else None
    custom_page.next_page = f"{base_url}sections/title/{section_title}?page={next_int}" if next_int else None

    return custom_page


@sections_router.get('/course/{course_id}', response_model=CustomPage)
def show_sections_by_course(
        course_id: int,
        request: Request,
        params: CustomParams = Depends(),
):
    base_url = str(request.base_url)

    # Retrieve token from cookies
    x_token = request.cookies.get('jwt_token')

    user_role = None
    user_id = None

    if x_token:
        logged_user = get_user_or_raise_401(x_token)
        user_id = logged_user.user_id
        user_role = logged_user.role

    sections_to_show = sections_services.grab_sections_by_course(course_id)

    paginated_sections = paginate(sections_to_show, params)

    # Create the custom page response
    custom_page = CustomPage.create(paginated_sections.items, paginated_sections.total, params)
    previous_int = custom_page.previous_page
    next_int = custom_page.next_page
    custom_page.previous_page = f"{base_url}sections/course/{course_id}?page={previous_int}" if previous_int else None
    custom_page.next_page = f"{base_url}sections/course/{course_id}?page={next_int}" if next_int else None

    return templates.TemplateResponse("sections/sections_by_course.html", {"request": request, "sections": paginated_sections.items, "previous_page": custom_page.previous_page, "next_page": custom_page.next_page})

@sections_router.get('/content/{section_id}', response_model=CustomPage)
def show_content_by_section(
        section_id: int,
        request: Request,
):
    x_token = request.cookies.get('jwt_token')
    section_content = sections_services.get_section_content(section_id)
    section_title = sections_services.get_section_title(section_id)

    if not section_content:
        raise HTTPException(status_code=404, detail="Section not found")
    return templates.TemplateResponse("sections/section_content.html", {"request": request, "section_content": section_content, "section_title": section_title})


#Only teachers that own the course can create new sections for it and update it
@sections_router.post('/new')
def create_section(section_data: Section, x_token: str = Header(None)):
    if x_token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You need to log in first!")

    user = get_user_or_raise_401(x_token)
    if user.role != "teacher":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only teachers can create sections!")

    course = courses_services.grab_any_course_by_id(section_data.course_id)
    if course.owner_id != user.user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="You need to be the owner of the course to add sections to it!")

    new_section = sections_services.create_section(section_data)
    return "New section created successfully!", new_section


@sections_router.put('/update/id/{section_id}')
def update_section(data: dict, section_id, x_token: str = Header()):
    user = get_user_or_raise_401(x_token)
    if data.get('section_id'):
        return "Section ID must be entered as a Path parameter."

    section = sections_services.grab_any_section_by_id(section_id)
    course = courses_services.grab_any_course_by_id(section.course_id)

    if user.role != "teacher" or course.owner_id != user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only teachers that own the course can update its sections!")

    sections_services.update_section(data, section_id)

    return "Section updated successfully!"


@sections_router.get('/any/{section_id}')
def experiment(section_id):
    sections_services.grab_any_section_by_id(section_id)