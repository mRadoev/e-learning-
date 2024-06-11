from datetime import datetime
from pydantic import BaseModel, constr, Field
from typing import List, Optional
from fastapi_pagination import Params, Page

TUsername = constr(pattern=r'^\w{2,30}$')


class CustomPage(BaseModel):
    items: list
    total: int
    page: int
    size: int
    previous_page: Optional[int] = None
    next_page: Optional[int] = None

    @classmethod
    def create(cls, items: [], total: int, params: Params):
        current_page = params.page
        page_size = params.size
        total_pages = (total + page_size - 1) // page_size

        previous_page = current_page - 1 if current_page > 1 else None
        next_page = current_page + 1 if current_page < total_pages else None

        return cls(
            items=items,
            total=total,
            page=current_page,
            size=page_size,
            previous_page=previous_page,
            next_page=next_page
        )


class CustomParams(Params):
    size: int = 10


class LoginData(BaseModel):
    email: str
    password: str


class Role:
    ADMIN = 'admin'
    TEACHER = 'teacher'
    STUDENT = 'student'
    GUEST = 'guest'


class User(BaseModel):
    user_id: int | None = None
    role: str = Field(..., pattern=r'^(admin|teacher|student|guest)$')
    email: str
    first_name: str
    last_name: str
    password: str
    photo: Optional[None] = None
    phone_number: Optional[str] = None
    linkedin: Optional[str] = None

    @classmethod
    def from_query_result(cls, user_id, role, email, first_name, last_name, password="Password is hidden."):
        return cls(
            user_id=user_id,
            role=role,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password
        )

    class Config:
        arbitrary_types_allowed = True


class Student(BaseModel):
    user_id: int
    photo: Optional[str] = None


class Course(BaseModel):
    course_id: int | None = None
    owner_id: int | None = None
    title: str
    description: str
    objectives: str
    tags: str
    status: int = 0  # 0 = public, 1 = premium

    def to_guest_dict(self):
        return self.dict(include={'course_id', 'title', 'description', 'tags', 'student_rating'})

    def to_user_dict(self):
        return self.dict(
            include={'course_id', 'title', 'description', 'objectives', 'owner_id', 'tags', 'status'})

    @classmethod
    def from_query_result(cls, course_id, owner_id, title, description, objectives, tags, status):
        return cls(
            course_id=course_id,
            owner_id=owner_id,
            title=title,
            description=description,
            objectives=objectives,
            tags=tags,
            status=status
        )

    class Config:
        arbitrary_types_allowed = True


class Section(BaseModel):
    course_id: int
    section_id: int
    title: str
    content: str
    description: str

    def to_guest_dict(self):
        return self.dict(include={'course_id', 'section_id', 'title', 'description'})

    def to_student_dict(self):
        return self.dict(include={'course_id', 'section_id', 'title', 'content', 'description'})

    def to_teacher_dict(self):
        return self.dict(
            include={'course_id', 'section_id', 'title', 'content', 'description'}
        )

    @classmethod
    def from_query_result(cls, course_id: str, section_id: Optional[str], title: str, content: str, description: str,
                          link: Optional[str] = None):

        try:
            course_id_int = int(course_id)
        except ValueError:
            course_id_int = None

        if section_id is not None:
            try:
                section_id_int = int(section_id)
            except ValueError:
                section_id_int = None
        else:
            section_id_int = None

        if description is None:
            description = "No description given yet"  # Providing a default value if description is None

        return cls(
            course_id=course_id_int,
            section_id=section_id_int,
            title=title,
            content=content,
            description=description,
            link=link
        )

    class Config:
        arbitrary_types_allowed = True


class Email(BaseModel):
    email_id: int | None = None
    sender_id: int
    recipient_id: int | None = None
    course_id: int
    response: bool | None = None

    @classmethod
    def from_query_result(cls, email_id, sender_id, recipient_id, course_id, response):
        return cls(email_id=email_id, sender_id=sender_id,
                   recipient_id=recipient_id, course_id=course_id, response=response)
