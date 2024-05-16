from fastapi import APIRouter, Response, status, HTTPException, Header, Query
from data.models import Section

section_router = APIRouter(prefix='/sections')


#Students can only view sections that are from public courses or premium courses that they have access to
#Guests cannot view sections
@section_router.get('/')
def show_sections(x_token: str = Header()):
    pass


@section_router.get('/id/{section_id}')
def show_section_by_id(section_id, x_token: str = Header()):
    pass


@section_router.get('/title/{section_title}')
def show_section_by_title(section_title, x_token: str = Header()):
    pass


#Only teachers that own the course can create new sections for it
@section_router.post('/new')
def create_section(data: Section, x_token: str = Header()):
    pass


@section_router.put('/update')
def update_section(data, x_token: str = Header()):
    pass
