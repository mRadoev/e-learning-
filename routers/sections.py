from fastapi import APIRouter, Response, status, HTTPException, Header, Query
from data.models import Section, Course, Role
from common.auth import get_user_or_raise_401
from services import sections_services
from typing import Optional

sections_router = APIRouter(prefix='/sections')


#Teachers can access all sections they own (only?)
#Students can only view sections that are from public courses or premium courses that they have access to
#Guests cannot view sections
#Pagination for sorting sections by id or name TO DO !!!
#Remove content from shown topic parameters, show only when looking for specific topic(submenu)
@sections_router.get('/')
def show_sections(x_token: Optional[str] = Header(None)):
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

    return courses

#Content can be made not visible, because it's supposed to be long text, so instead by searching
#for the section by id or name you can view the full content of the section.
@sections_router.get('/id/{section_id}')
def show_section_by_id(section_id, x_token: str = Header()):
    pass


@sections_router.get('/title/{section_title}')
def show_section_by_title(section_title, x_token: str = Header()):
    pass


#Only teachers that own the course can create new sections for it and update it
@sections_router.post('/new')
def create_section(data: Section, x_token: str = Header()):
    pass


@sections_router.put('/update')
def update_section(data, x_token: str = Header()):
    pass
