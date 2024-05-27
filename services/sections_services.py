from data.database import read_query, insert_query, delete_query
from data.models import Course, Section  # CourseHasUsers
from services.users_services import decode_token
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
                            JOIN students_has_courses sc ON sc.course_id = s.course_id
                            WHERE c.status = 1 AND sc.user_id = {user_id}
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
                            WHERE c.status = 1 AND c.owner_id = {user_id}
                            UNION ALL
                            SELECT s.course_id, s.section_id, s.title, s.content, s.description, s.link 
                            FROM sections s
                            JOIN courses c ON c.course_id = s.course_id
                            WHERE c.status = 0
                            ORDER BY course_id;''')
    sections = [Section.from_query_result(*row) for row in data]
    return sections


def admin_view():
    data = read_query('''SELECT s.course_id, s.section_id, s.title, s.content, s.description, s.link 
                        FROM sections s
                        ORDER BY course_id''')
    sections = [Section.from_query_result(*row) for row in data]
    return sections
