from fastapi import APIRouter, Response, status, HTTPException, Header, Query

section_router = APIRouter(prefix='/sections')


@section_router.get('/')
def show_sections(x_token: str = Header()):
    pass


@section_router.get('/id/{section_id}')
def show_section_by_id(section_id, x_token: str = Header()):
    pass


@section_router.get('/title/{section_title}')
def show_section_by_title(section_title, x_token: str = Header()):
    pass