from datetime import datetime
from pydantic import BaseModel, constr

TUsername = constr(pattern='^\w{2,30}$')


class LoginData(BaseModel):
    email: TUsername
    password: str


class Role:
    ADMIN = 'admin'
    TEACHER = 'teacher'
    STUDENT = 'student'
    GUEST = 'guest'


class User(BaseModel):
    user_id: int
    role: Role = None
    email: str
    first_name: str
    last_name: str
    password: str
    photo: None
    phone_number: int | None
    linkedin: str | None

    @classmethod
    def from_query_result(cls, user_id, role, email, first_name, last_name, password):
        return cls(
            user_id=user_id,
            role=role,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password
        )


class Course(BaseModel):
    course_id: int
    title: str
    description: str
    objectives: str
    owner: User
    tags: [str]
    status: int # 0 = public, 1 = premium
    students_rating: int # The average of the sum of each student who gave the course a rating
    #optional homepage picture

    @classmethod
    def from_query_result(cls, course_id, title, description, objectives, owner, tags, status, students_rating):
        return cls(
            course_id=course_id,
            title=title,
            description=description,
            objectives=objectives,
            owner=owner,
            tags=tags,
            status=status,
            students_rating=students_rating
        )


class Section(BaseModel):
    section_id: int
    course_id: int
    title: str
    content: str
    description: str
    link: str

    @classmethod
    def from_query_result(cls, section_id, course_id, title, content, description, link):
        return cls(
            section_id=section_id,
            course_id=course_id,
            title=title,
            content=content,
            description=description,
            link=link
        )


class CourseHasUsers(BaseModel):
    course_id: int
    user_id: int
    has_control: int
    has_access: int
    student_rating: int
