from data.database import read_query, insert_query, delete_query
from data.models import Course  # CourseHasUsers
from services.users_services import decode_token, get_user_role_from_token
from common import auth
from fastapi import HTTPException, status, Header


def find_sender_id(x_token: str = Header(...)) -> int:
    data = decode_token(x_token)
    user_id = data.get('id')
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token: User ID not found"
        )
    return user_id


def guest_view():
    data = read_query('SELECT c.course_id, c.title, c.description, c.objectives, c.owner, c.tags, c.student_rating '
                      'FROM courses AS c WHERE c.status = 0')
    return next((Course.from_query_result(*row) for row in data), None)


def student_view(user_id: int):
    data = read_query(f'''SELECT c.course_id, c.title, c.description, c.objectives, c.owner, c.tags, c.student_rating
                        FROM courses c 
                        WHERE c.status = 0
                        UNION ALL
                        SELECT c.course_id, c.title, c.description, c.objectives, c.owner, c.tags, c.student_rating
                        FROM courses c 
                        JOIN courses_has_users cu ON c.course_id = cu.course_id
                        WHERE c.status = 1 AND cu.user_id = {user_id} AND cu.has_access = 1
                        ORDER BY course_id;''')
    return next((Course.from_query_result(*row) for row in data), None)


def admin_view(user):
    data = read_query('SELECT * FROM courses')
    return next((Course.from_query_result(*row) for row in data), None)


def teacher_view(user_id: int):
    data = read_query(f'''SELECT c.course_id, c.title, c.description, c.objectives, c.owner, c.tags, c.student_rating
                        FROM courses c 
                        WHERE c.status = 0
                        UNION ALL
                        SELECT c.course_id, c.title, c.description, c.objectives, c.owner, c.tags, c.student_rating
                        FROM courses c 
                        JOIN courses_has_users cu ON c.course_id = cu.course_id
                        WHERE c.status = 1 AND cu.user_id = {user_id} AND cu.has_control = 1
                        ORDER BY course_id;''')
    return next((Course.from_query_result(*row) for row in data), None)

# def show_course_by_id(course_id: int, user_role: str, user_id: int) -> Course:
#     if user_role == 'guest':
#         courses = guest_view()
#     elif user_role == 'student':
#         courses = student_view(user_id)
#     else:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
#
#     course_data = next((course for course in courses if course['course_id'] == course_id), None)
#
#     if not course_data:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
#     course = Course(**course_data)
#     return course


def create_course(course: Course, user_role: str) -> Course:
    if user_role != "teacher":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only teachers can create courses")

    generated_id = insert_query(
        'INSERT INTO courses(title, description, objectives, owner, tags, status, students_rating) VALUES (?, ?, ?, ?, ?, ?, ?)',
        (course.title, course.description, course.objectives, course.owner, ','.join(course.tags), course.status, course.students_rating)
    )
    course.course_id = generated_id

    return course


def delete_course(course_id: int, title: str, token: str):
    user_role = get_user_role_from_token(token)
    user_id = auth.get_user_or_raise_401(token).user_id

    if user_role != "teacher" or "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only teachers can delete courses")

    if course_id is not None and user_role == "admin":
        delete = "DELETE FROM courses WHERE course_id = ?"
        delete_params = (course_id,)
    elif title is not None and user_role == "admin":
        delete = "DELETE FROM courses WHERE title = ?"
        delete_params = (title,)


    # elif title is not None and user_role == "teacher":
        #pass

    elif course_id is not None and user_role == "teacher":
        delete_query(''' DELETE cu
                            FROM courses_has_users cu
                            JOIN courses c ON cu.course_id = c.course_id
                            WHERE cu.course_id = ? AND cu.has_control = 1 AND cu.user_id = ?;
                            
                            DELETE cu
                            FROM courses_has_users cu
                            WHERE cu.course_id = ?;
                            
                            DELETE s
                            FROM sections s
                            WHERE s.course_id = ?;
                            
                            DELETE courses
                            FROM courses
                            WHERE courses.course_id = ?;''',
                          (course_id, user_id, course_id, course_id, course_id))
        return "Course deleted successfully!"

    else:
        raise ValueError("Provide either course_id or title to delete a course")
    success = delete_query(delete, delete_params)
    if success:
        return "Course deleted successfully"
