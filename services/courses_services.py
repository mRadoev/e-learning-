from data.database import read_query, update_query, insert_query
from data.models import Course, User #CourseHasUsers


def guest_view():
    data = read_query('SELECT course_id, title, description, objectives, owner, tags, student_rating'
                      'FROM courses c WHERE c.status = 0')
    return data


def student_view(student_id: int):
    data = read_query('SELECT course_id, title, description, objectives, owner, tags, student_rating'
                      'FROM courses c WHERE c.status = 0')
    pass

def admin_view(user):
    pass

def teacher_view(user):
    pass