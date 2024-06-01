# e-learning-
## 1. Project description
- Desinged and implemented an E-Learning platform.
- Provided a RESTful API that can be consumed by different clients.
- High-level description:
    - Administrators manage teachers, students, courses and sections
    - Students can read courses and their sections if they have premium access or the course is public
    - Teachers can create/delete courses and sections to courses they own
    - Students can rate each course

## 2. Database - relationships between tables

[//]: # (![image]&#40;https://github.com/mRadoev/e-learning-/assets/155682021/ea913bda-425d-4887-b4a8-3a93ef1a4e88&#41;)
![Untitled.png](Untitled.png)

## 3. Endpoints
### 3.1. Courses
- ✔ Get /courses:
    
-`http://127.0.0.1:8000/courses`

Shows all public courses if no user is logged in.

-`http://127.0.0.1:8000/courses`
with jwt token for admin:
```json
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJmaXJzdF9uYW1lIjoiYWRtaW4iLCJsYXN0X25hbWUiOiJhZG1pbiIsImVtYWlsIjoiZXhhbXBsZTEwQGFzZC5jb20iLCJyb2xlIjoiYWRtaW4iLCJwYXNzd29yZCI6ImFkbWluIn0.52A-HsBOMLwRcpSWdHGBBo6-PYW32WnbPMwKkfLnCOU
```
Shows all courses with all details if the admin is logged in.

