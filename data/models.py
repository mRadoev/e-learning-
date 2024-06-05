from datetime import datetime
from pydantic import BaseModel, constr, Field
from typing import List, Optional

TUsername = constr(pattern=r'^\w{2,30}$')


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
    password: str = "Password is hidden."
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


class Course(BaseModel):
    course_id: int | None = None
    owner_id: int | None = None
    title: str
    description: str
    objectives: str
    tags: str
    status: int = 0  # 0 = public, 1 = premium
    # student_rating: int | str = None  # The average of the sum of each student who gave the course a rating

    def to_guest_dict(self):
        return self.dict(include={'course_id', 'title', 'description', 'tags', 'student_rating'})

    def to_student_dict(self):
        return self.dict(include={'course_id', 'title', 'description', 'objectives', 'owner_id', 'tags'})

    def to_teacher_dict(self):
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
    section_id: int | None = None
    title: str
    content: str
    description: str = "No description given yet"
    link: str = "No link given yet"

    @classmethod
    def from_query_result(cls, course_id, section_id, title, content, description, link):
        return cls(
            course_id=course_id,
            section_id=section_id,
            title=title,
            content=content,
            description=description,
            link=link
        )

    class Config:
        arbitrary_types_allowed = True


class Email(BaseModel):
    email_id: int
    sender_id: int
    recipient_id: int | None = None
    course_id: int
    response: bool | None = None

    @classmethod
    def from_query_result(cls, email_id, sender_id, recipient_id, course_id, response):
        return cls(email_id=email_id, sender_id=sender_id,
                   recipient_id=recipient_id, course_id=course_id, response=response)

                          # class Student:

# class Teacher:



# class Message(BaseModel):
#     message_id: int | None = None
#     sender_email: str
#     recipient_email: str
#     message_text: str
#
#     @classmethod
#     def from_query_result(cls, message_id, sender_email, recipient_email, message_text):
#         return cls(
#             message_id=message_id,
#             sender_email=sender_email,
#             recipient_email=recipient_email,
#             message_text=message_text)
#
#
# class MessagePayload(BaseModel):
#     recipient_email: str
#     message_text: str
