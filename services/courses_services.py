from data.database import read_query, insert_query, delete_query, update_query
from data.models import Course, Email, User  # CourseHasUsers
from services.users_services import decode_token
from common import auth
from fastapi import HTTPException, status, Header


def guest_view():
    data = read_query('SELECT c.course_id, owner_id, c.title, c.description, c.objectives, c.tags, c.status '
                      'FROM courses AS c WHERE c.status = 0')
    courses = [Course.from_query_result(*row) for row in data]
    return [course.to_guest_dict() for course in courses]


def student_view(user_id: int):
    data = read_query(f'''SELECT c.course_id, owner_id, c.title, c.description, c.objectives, c.tags, c.status
                            FROM courses c 
                            WHERE c.status = 0
                            UNION ALL
                            SELECT c.course_id, owner_id, c.title, c.description, c.objectives, c.tags, c.status 
                            FROM courses c
                            JOIN students_has_courses sc ON c.course_id = sc.course_id
                            WHERE c.status = 1 AND sc.user_id = {user_id}
                            ORDER BY course_id;''')
    courses = [Course.from_query_result(*row) for row in data]
    return [course.to_student_dict() for course in courses]


def teacher_view(user_id: int):
    data = read_query(f'''SELECT c.course_id, owner_id, c.title, c.description, c.objectives, c.tags, c.status
                            FROM courses c 
                            WHERE c.status = 0
                            OR c.owner_id = {user_id}''')
    courses = [Course.from_query_result(*row) for row in data]
    return [course.to_teacher_dict() for course in courses]


def admin_view():
    data = read_query('''SELECT c.course_id, c.owner_id, c.title, c.description, c.objectives, c.tags, c.status 
                            FROM courses c ''')
    return [Course.from_query_result(*row) for row in data]


def grab_any_course_by_id(course_id: int) -> Course:
    data = read_query(f'''SELECT c.course_id, c.owner_id, c.title, c.description, c.objectives, c.tags, c.status 
                            FROM courses c WHERE course_id = {course_id}''')
    course = next((Course.from_query_result(*row) for row in data), None)
    if course:
        return course
    raise HTTPException(status_code=404, detail="Course not found")


def by_id_for_guest(course_id: int):
    data = read_query(f'''SELECT c.course_id, c.owner_id, c.title, c.description, c.objectives, c.tags, c.status 
                            FROM courses c
                            WHERE c.status = 0 AND c.course_id = {course_id};''')
    shown_course = next((Course.from_query_result(*row) for row in data), None)
    return shown_course.to_guest_dict()


def by_id_for_non_guest(course_id):
    data = read_query(f'''SELECT c.course_id, c.owner_id, c.title, c.description, c.objectives, c.tags, c.status 
                            FROM courses c
                            WHERE c.status = 0 AND c.course_id = {course_id};''')
    shown_course = next((Course.from_query_result(*row) for row in data), None)
    return shown_course.to_student_dict()


def by_id_for_student(student_id, course_id):
    data = read_query(f'''SELECT c.course_id, c.owner_id, c.title, c.description, c.objectives, c.tags, c.status
                            FROM courses c
                            JOIN students_has_courses sc ON sc.course_id = c.course_id
                            WHERE c.status = 1 AND c.course_id = {course_id} AND sc.user_id = {student_id}
                            UNION ALL
                            SELECT c.course_id, c.owner_id, c.title, c.description, c.objectives, c.tags, c.status
                            FROM courses c
                            WHERE c.status = 0 AND c.course_id = {course_id}''')
    shown_course = next((Course.from_query_result(*row) for row in data), None)
    return shown_course.to_student_dict()


def by_id_for_teacher(teacher_id, course_id):
    data = read_query(f'''SELECT c.course_id, c.owner_id, c.title, c.description, c.objectives, c.tags, c.status
                            FROM courses c
                            WHERE (c.owner_id = {teacher_id} AND c.course_id = {course_id})
                            OR (c.status = 0 AND c.course_id = {course_id})''')
    shown_course = next((Course.from_query_result(*row) for row in data), None)
    return shown_course.to_teacher_dict()


def by_title_for_guest(course_title: str):
    data = read_query(f'''SELECT c.course_id, c.owner_id, c.title, c.description, c.objectives, c.tags, c.status 
                            FROM courses c
                            WHERE title LIKE '%{course_title}%'
                            AND c.status = 0 ''')
    courses = [Course.from_query_result(*row) for row in data]
    return [course.to_guest_dict() for course in courses]


def by_title_for_student(course_title: str, user_id: int):
    data = read_query(f'''SELECT c.course_id, c.owner_id, c.title, c.description, c.objectives, c.tags, c.status 
                            FROM courses c
                            WHERE title LIKE '%{course_title}%'
                            AND c.status = 0 
                            UNION ALL 
                            SELECT c.course_id, c.owner_id, c.title, c.description, c.objectives, c.tags, c.status 
                            FROM courses c 
                            JOIN students_has_courses sc ON sc.course_id = c.course_id 
                            WHERE c.title LIKE '%{course_title}%' AND c.status = 1 AND sc.user_id = {user_id};''')
    courses = [Course.from_query_result(*row) for row in data]
    return [course.to_student_dict() for course in courses]


def by_title_for_teacher(section_title: str, user_id: int):
    data = read_query(f'''SELECT s.section_id, s.course_id, s.title, s.content, s.description 
                            FROM sections s
                            JOIN courses c 
                            ON s.course_id = c.course_id
                            WHERE s.title LIKE '%{section_title}%' 
                            AND c.status = 0 
                            UNION ALL 
                            SELECT s.section_id, s.course_id, s.title, s.content, s.description 
                            FROM sections s 
                            JOIN courses c 
                            ON s.course_id = c.course_id 
                            WHERE s.title LIKE '%{section_title}%' 
                            AND c.status = 1 AND c.owner_id = {user_id};''')
    sections = [Course.from_query_result(*row) for row in data]
    return [section.to_teacher_dict() for section in sections]


def by_title_for_admin(course_title: str):
    data = read_query(f'''SELECT c.course_id, c.owner_id, c.title, c.description, c.objectives, c.tags, c.status 
                        FROM courses c 
                        WHERE title LIKE "%{course_title}%"''')
    courses = [Course.from_query_result(*row) for row in data]
    return courses


def by_tag_for_guest(tag: str):
    data = read_query(f'''SELECT c.course_id, c.owner_id, c.title, c.description, c.objectives, c.tags, c.status 
                        FROM courses c
                        WHERE c.tags LIKE "%{tag}%" AND c.status = 0''')
    courses = [Course.from_query_result(*row) for row in data]
    return [course.to_guest_dict() for course in courses]


def by_tag_for_student(tag: str, student_id: int):
    data = read_query(f'''SELECT c.course_id, c.owner_id, c.title, c.description, c.objectives, c.tags, c.status 
                        FROM courses c
                        WHERE c.tags LIKE "%{tag}%" AND c.status = 0
                        UNION ALL
                        SELECT c.course_id, c.owner_id, c.title, c.description, c.objectives, c.tags, c.status 
                        FROM courses c
                        JOIN students_has_courses sc ON sc.course_id = c.course_id
                        WHERE c.tags LIKE "%{tag}%" AND c.status = 1 AND sc.user_id = {student_id}''')
    courses = [Course.from_query_result(*row) for row in data]
    return [course.to_student_dict() for course in courses]


def by_tag_for_teacher(tag: str, teacher_id: int):
    data = read_query(f'''SELECT c.course_id, c.owner_id, c.title, c.description, c.objectives, c.tags, c.status 
                        FROM courses c
                        WHERE c.tags LIKE "%{tag}%" AND c.status = 0
                        UNION ALL
                        SELECT c.course_id, c.owner_id, c.title, c.description, c.objectives, c.tags, c.status 
                        FROM courses c
                        WHERE c.tags LIKE "%{tag}%" AND c.status = 1 AND c.owner_id = {teacher_id}''')
    courses = [Course.from_query_result(*row) for row in data]
    return [course.to_teacher_dict() for course in courses]


def by_tag_for_admin(tag: str):
    data = read_query(f'''SELECT c.course_id, c.owner_id, c.title, c.description, c.objectives, c.tags, c.status 
                        FROM courses c
                        WHERE c.tags LIKE "%{tag}%"''')
    courses = [Course.from_query_result(*row) for row in data]
    return courses


def create_course(course: Course, owner_id: int) -> Course:
    generated_id = insert_query(
        'INSERT INTO courses(title, owner_id,description, objectives, tags, status) VALUES(?, ?, ?, ?, ?, ?)',
        (course.title, owner_id, course.description, course.objectives, course.tags, course.status)
    )
    course.course_id = generated_id
    course.owner_id = owner_id
    return course


def delete_course(course_id: int, token: str):
    user = auth.get_user_or_raise_401(token)
    user_id = user.user_id

    if user.role != ("teacher" or "admin"):
        raise HTTPException(status_code=403, detail="You do not have access to delete rights!")

    #TO DO
    if course_id is not None and user.role == "admin":
        delete_query(f''' DELETE sc
                            FROM students_has_courses sc
                            WHERE sc.course_id = ?;
                            
                            DELETE s
                            FROM sections s
                            WHERE s.course_id = ?;
                            
                            DELETE courses
                            FROM courses
                            WHERE courses.course_id = ?;''')


    elif course_id is not None and user.role == "teacher":
        data = read_query(f'''SELECT * 
                                FROM courses c 
                                WHERE c.owner_id = {user_id}AND c.course_id = {course_id} ''')
        if data:
            delete_query(f''' DELETE sc
                                FROM students_has_courses sc
                                WHERE sc.course_id = {course_id}''')
            delete_query(f'''DELETE s
                                FROM sections s
                                WHERE s.course_id = {course_id};
                                
                                DELETE courses
                                FROM courses
                                WHERE courses.course_id = {course_id}''')
            return "Course deleted successfully!"

        return f"Course with id #{course_id} not found."

    else:
        raise ValueError("Provide either course_id or title to delete a course")
    return "Course NOT deleted successfully"


def check_premium_limit_reached(student_id: int):
    data = read_query(f'''SELECT course_id
                        FROM students_has_courses sc
                        WHERE sc.user_id = {student_id}''')  #AND sc.status = 1
    premium_courses = 0
    for row in data:
        premium_courses += 1
    if premium_courses >= 5:
        raise HTTPException(status_code=403,
                            detail="You have reached your premium course enrollment limit of 5")


def update_course(data: dict, course_id: int):
    for key, value in data.items():
        if type(value) is str:
            value = '"' + f'{value}' + '"'
        update_query(f'''UPDATE courses
                        SET {key} = {value} 
                        WHERE course_id = {course_id}''')


def send_enrollment_request(sender_id: int, course_id: int):
    course = grab_any_course_by_id(course_id)
    recipient_id = course.owner_id

    # fetch the teacher with control over course
    data = read_query(f'''SELECT c.owner_id
                            FROM courses c
                            WHERE c.course_id = {course_id}
                            ''')

    enrollment_exists = read_query(f'''SELECT *
                            FROM emails e
                            WHERE e.sender_id = {sender_id} 
                            AND e.recipient_id = {recipient_id} AND e.course_id = {course_id}
                            ''')

    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    teacher_id = data[0][0]

    if not enrollment_exists:
        insert_query(
            f'''
            INSERT INTO emails (sender_id, recipient_id, course_id)
            VALUES ({sender_id}, {teacher_id}, {course_id})
            ''')

        return "Enrollment request sent successfully"

    return "You have already enrolled for this course!"


def unsubscribe_from_course(user_id: int, course_id: int):
    enrollment_exists = read_query(f'''
        SELECT *
        FROM students_has_courses sc
        WHERE sc.course_id = {course_id} AND sc.user_id = {user_id}
    ''')

    if not enrollment_exists:
        return "You are not enrolled in this course."

    # Delete the enrollment record
    delete_query(f'''DELETE FROM students_has_courses
                    WHERE course_id = {course_id} AND user_id = {user_id}''')

    return "Unsubscribed from the course successfully."


def show_pending_requests(user_id):
    data = read_query(f'''SELECT * 
                        FROM emails e
                        WHERE e.recipient_id = {user_id} AND e.response IS NULL;''')
    emails = [Email.from_query_result(*row) for row in data]
    return emails


################################# Test
def respond_to_request(course_id: int, student_id: int, response: bool):
    data = read_query(f'''SELECT * 
                    FROM students_has_courses sc 
                    WHERE sc.user_id = {student_id} AND sc.course_id = {course_id}''')
    update_query(f'''UPDATE emails e
                    SET e.response = {response}
                    WHERE e.sender_id = {student_id} AND e.course_id = {course_id}''')
    if response and not data:
        insert_query(f'''INSERT INTO students_has_courses(course_id, user_id, subscription_status) 
        VALUES({course_id}, {student_id}, 1)''')

    elif not response and data:
        update_query(f'''UPDATE students_has_courses sc
                    SET sc.subscription_status = 0
                    WHERE sc.user_id = {student_id} AND sc.course_id = {course_id}''')


def get_course_user_admin(course_id: int):
    data = read_query(f'''SELECT u.user_id, u.role, u.email, u.first_name, u.last_name, u.password 
                    FROM users u 
                    JOIN students_has_courses sc 
                    ON u.user_id = sc.user_id 
                    WHERE sc.course_id = {course_id}''')

    users = [User.from_query_result(*row) for row in data]
    return users


def get_course_user_teacher(course_id: int, user_id: int):
    data = read_query(f'''SELECT DISTINCT u.user_id, u.role, u.email, u.first_name, u.last_name, u.password
                    FROM users u
                    JOIN students_has_courses sc
                    JOIN courses c
                    ON u.user_id = sc.user_id 
                    WHERE sc.course_id = {course_id}
                    AND c.owner_id = {user_id}''')

    users = [User.from_query_result(*row) for row in data]
    return users


#Report needs to indicate which students are still enrolled and which aren't
def generate_report(course_id: int):
    data = read_query(f'''SELECT u.user_id, u.role, u.email, u.first_name, u.last_name, u.password
                    FROM users u
                    JOIN students_has_courses sc ON sc.user_id = u.user_id
                    WHERE sc.course_id = {course_id}
                    ORDER BY sc.subscription_status''')

    users = [User.from_query_result(*row) for row in data]
    return users
