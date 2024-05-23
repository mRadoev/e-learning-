from data.database import read_query, insert_query, delete_query
from data.models import Course, Section  # CourseHasUsers
from services.users_services import decode_token, get_user_role_from_token
from common import auth
from fastapi import HTTPException, status, Header


def guest_view():
    data = read_query('''SELECT s.course_id, s.section_id, s.title, s.content, s.description, s.link 
                        FROM sections s
                        JOIN courses c ON c.course_id = s.course_id
                        WHERE c.status = 0;''')
    sections = [Section.from_query_result(*row) for row in data]
    return sections


#############################
def student_view(user_id: int):
    data = read_query(f'''SELECT s.course_id, s.section_id, s.title, s.content, s.description, s.link
                        FROM sections s
                        JOIN courses c ON c.course_id = s.course_id
                        JOIN courses_has_users cu ON cu.course_id = s.course_id
                        WHERE c.status = 1 AND cu.has_access = 1 AND cu.user_id = {user_id}
                        UNION ALL
                        SELECT s.course_id, s.section_id, s.title, s.content, s.description, s.link 
                        FROM sections s
                        JOIN courses c ON c.course_id = s.course_id
                        WHERE c.status = 0
                        ORDER BY course_id;''')
    sections = [Section.from_query_result(*row) for row in data]
    return sections


def teacher_view(user_id: int):
    data = read_query(f'''SELECT s.course_id, s.section_id, s.title, s.content, s.description, s.link
                        FROM sections s
                        JOIN courses c ON c.course_id = s.course_id
                        JOIN courses_has_users cu ON cu.course_id = s.course_id
                        WHERE c.status = 1 AND cu.has_control = 1 AND cu.user_id = {user_id}
                        UNION ALL
                        SELECT s.course_id, s.section_id, s.title, s.content, s.description, s.link 
                        FROM sections s
                        JOIN courses c ON c.course_id = s.course_id
                        WHERE c.status = 0
                        ORDER BY course_id;''')
    sections = [Section.from_query_result(*row) for row in data]
    return sections


def admin_view(user_id: int):
    data = read_query('''SELECT s.course_id, s.section_id, s.title, s.content, s.description, s.link 
                        FROM sections s''')
    return next((Section.from_query_result(*row) for row in data), None)