from data.database import read_query, insert_query, delete_query
from data.models import Course  # CourseHasUsers
from users_services import decode_token, get_user_role_from_token
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


def student_view(student_id: int):
    data = read_query('SELECT c.course_id, c.title, c.description, c.objectives, c.owner, c.tags, c.student_rating '
                      'FROM courses c WHERE c.status = 0')
    return next((Course.from_query_result(*row) for row in data), None)


def admin_view(user):
    pass


def teacher_view(user):
    pass

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
    if user_role != "teacher" or "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only teachers can delete courses")

    if course_id is not None:
        delete = "DELETE FROM courses WHERE course_id = ?"
        delete_params = (course_id,)
    elif title is not None:
        delete = "DELETE FROM courses WHERE title = ?"
        delete_params = (title,)
    else:
        raise ValueError("Provide either course_id or title to delete a course")
    success = delete_query(delete, delete_params)
    if success:
        return "Course deleted successfully"
