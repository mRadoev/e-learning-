from data.database import read_query, insert_query, delete_query
from data.models import Course  # CourseHasUsers
from services.users_services import decode_token
from common import auth
from fastapi import HTTPException, status, Header


#Do we need if we can find user by token instead of just id?
# def find_sender_id(x_token: str = Header(...)) -> int:
#     user = decode_token(x_token)
#     user_id = user.get('id')
#     return user_id


def guest_view():
    data = read_query('SELECT * '
                      'FROM courses AS c WHERE c.status = 0')
    courses = [Course.from_query_result(*row) for row in data]
    return [course.to_guest_dict() for course in courses]


def student_view(user_id: int):
    data = read_query(f'''SELECT c.course_id, c.title, c.description, c.objectives, c.owner, c.tags, c.status, c.student_rating
                        FROM courses c 
                        WHERE c.status = 0
                        UNION ALL
                        SELECT c.course_id, c.title, c.description, c.objectives, c.owner, c.tags, c.status, c.student_rating
                        FROM courses c 
                        JOIN courses_has_users cu ON c.course_id = cu.course_id
                        WHERE c.status = 1 AND cu.user_id = {user_id} AND cu.has_access = 1
                        ORDER BY course_id;''')
    courses = [Course.from_query_result(*row) for row in data]
    return [course.to_student_dict() for course in courses]


def teacher_view(user_id: int):
    data = read_query(f'''SELECT c.course_id, c.title, c.description, c.objectives, c.owner, c.tags, c.status, c.student_rating
                        FROM courses c 
                        WHERE c.status = 0
                        UNION ALL
                        SELECT c.course_id, c.title, c.description, c.objectives, c.owner, c.tags, c.status, c.student_rating
                        FROM courses c 
                        JOIN courses_has_users cu ON c.course_id = cu.course_id
                        WHERE c.status = 1 AND cu.user_id = {user_id} AND cu.has_control = 1
                        ORDER BY course_id;''')
    courses = [Course.from_query_result(*row) for row in data]
    return [course.to_teacher_dict() for course in courses]


def admin_view(user):
    data = read_query('SELECT * FROM courses')
    return [Course.from_query_result(*row) for row in data]


def grab_any_course_by_id(course_id: int):
    data = read_query(f'SELECT * FROM courses WHERE course_id = {course_id}')
    # course = [Course.from_query_result(*row) for row in data]
    course = next((Course.from_query_result(*row) for row in data), None)
    if course:
        return course
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")


def by_id_for_guest(course_id):
    data = read_query(f'''SELECT * 
                        FROM courses c
                        WHERE c.status = 0 AND c.course_id = {course_id};''')
    shown_course = next((Course.from_query_result(*row) for row in data), None)
    return shown_course.to_guest_dict()


def by_id_for_non_guest(course_id):
    data = read_query(f'''SELECT * 
                        FROM courses c
                        WHERE c.status = 0 AND c.course_id = {course_id};''')
    shown_course = next((Course.from_query_result(*row) for row in data), None)
    return shown_course.to_student_dict()


def by_id_for_student(student_id, course_id):
    data = read_query(f'''SELECT c.course_id, c.title, c.description, c.objectives, c.owner, c.tags, c.status, c.student_rating
                        FROM courses c
                        JOIN courses_has_users cu ON cu.course_id = c.course_id
                        WHERE c.status = 1 AND cu.has_access = 1 AND c.course_id = {course_id} AND cu.user_id = {student_id};''')
    shown_course = next((Course.from_query_result(*row) for row in data), None)
    return shown_course.to_student_dict()


def by_id_for_teacher(teacher_id, course_id):
    data = read_query(f'''SELECT c.course_id, c.title, c.description, c.objectives, c.owner, c.tags, c.status, c.student_rating 
                        FROM courses c
                        JOIN courses_has_users cu ON cu.course_id = c.course_id
                        WHERE c.status = 1 AND cu.has_control = 1 AND c.course_id = {course_id} AND cu.user_id = {teacher_id};''')
    shown_course = next((Course.from_query_result(*row) for row in data), None)
    return shown_course.to_teacher_dict()


def create_course(course: Course) -> Course:
    generated_id = insert_query(
        'INSERT INTO courses(title, description, objectives, owner, tags, status, students_rating) VALUES (?, ?, ?, ?, ?, ?, ?)',
        (course.title, course.description, course.objectives, course.owner, ','.join(course.tags), course.status,
         course.students_rating)
    )
    course.course_id = generated_id

    return course


def delete_course(course_id: int, token: str):
    user = auth.get_user_or_raise_401(token)
    user_id = user.user_id

    if user.role != ("teacher" or "admin"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have access to delete rights!")

    #TO DO
    if course_id is not None and user.role == "admin":
        delete_query(f''' DELETE cu
                        FROM courses_has_users cu
                        WHERE cu.course_id = ?;
                        
                        DELETE s
                        FROM sections s
                        WHERE s.course_id = ?;
                        
                        DELETE courses
                        FROM courses
                        WHERE courses.course_id = ?;''')

    ###
    # elif title is not None and user_role == "teacher":
    #pass

    elif course_id is not None and user.role == "teacher":
        data = read_query(f'''SELECT * 
                            FROM courses_has_users cu
                            WHERE cu.course_id = 1 AND cu.has_control = 1 AND cu.user_id = {user_id}''')
        if data:
            delete_query(''' DELETE cu
                                FROM courses_has_users cu
                                WHERE cu.course_id = ? AND cu.has_control = 1 AND cu.user_id = ?;
                            ''', (course_id, user_id))
            delete_query('''DELETE s
                                FROM sections s
                                WHERE s.course_id = ?;
                                
                                DELETE courses
                                FROM courses
                                WHERE courses.course_id = ?;''',
                         (course_id, course_id, course_id))
            return "Course deleted successfully!"

        return f"Course with id #{course_id} not found."

    else:
        raise ValueError("Provide either course_id or title to delete a course")
    return "Course NOT deleted successfully"


def send_enrollment_request(sender_id: int, course_id: int):
    # fetch the teacher with control over course
    query = f'''
            SELECT u.user_id as teacher_id
            FROM courses_has_users chu
            JOIN users u ON chu.user_id = u.user_id
            WHERE chu.course_id = {course_id} AND chu.has_control = 1
        '''
    teacher_data = read_query(query, (course_id,))

    if not teacher_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No teacher found with control over the course")

    teacher_id = teacher_data[0]['user_id']

    insert_query(
        '''
        INSERT INTO emails (sender_id, recipient_id, enrollment_request)
        VALUES (?, ?, ?)
        ''',
        (sender_id, teacher_id, 1)
    )

    return "Enrollment request sent successfully"

