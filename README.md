# e-learning-
## 1. Project description
- Desinged and implemented an E-Learning platform.
- Provided a RESTful API that can be consumed by different clients.
- High-level description:
    - Administrators manage teachers, students, courses and sections
    - Students can read courses and their sections if they have premium access or the course is public
    - Teachers can create/delete courses and sections to courses they own
    - Students can rate each course

## 2. Instructions for Running the App

After downloading the code provided, you can see that there is a text file called `requirements.txt`. It contains all the packages and libraries needed in order to properly run the app. You can install these dependencies using pip:

```bash
pip install -r requirements.txt
```
Once you have executed this command, the whole functionality of the project should be available to you.
Another really important part of the startup is loading the database on your device. This happens by opening the `first_schema.sql` file, copying its content and pasting it in MySQL. Now, once you run the SQL, the whole schema is loaded on your device and you can start filling it with information.
It is important to mention that, the database does not load with base information, it is empty. In order to take fill it with some test information you can open the `schema_examples.sql` file and, once again, copy and paste its content. This put some test information in the database, so you can put the app to use


By running the `main.py` file you start up the whole app. Now you can access the "front end" from your browser.
## 3. Backend Structure

The backend structure of the E-Learning platform is organized into several folders:

- **common**: This folder contains common functionalities such as responses and authorization functions.
- **data**: The `data` folder is responsible for handling database connections and defining models used throughout the code.
- **routers**: Here, you'll find the endpoints for API requests. Each endpoint is responsible for a specific functionality.
- **services**: The `services` folder contains the business logic behind the endpoints defined in the `routers` folder.
- **templates**: This folder contains the HTML files which make the visualisation of each page of the app possible. 

Both the `routers` and `services` folders are further divided into subfolders, each dedicated to functionality related to users, courses, and sections of the courses.

## 4. Database - relationships between tables

[//]: # (![image]&#40;https://github.com/mRadoev/e-learning-/assets/155682021/ea913bda-425d-4887-b4a8-3a93ef1a4e88&#41;)
![schema.png](schema.png)

## 5. Endpoints
### 5.1. Courses
- ✔ Get /courses:
    
-`http://127.0.0.1:8000/courses`

Shows all public courses if no user is logged in.

-`http://127.0.0.1:8000/courses`
with jwt token for admin:
```json
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJmaXJzdF9uYW1lIjoiYWRtaW4iLCJsYXN0X25hbWUiOiJhZG1pbiIsImVtYWlsIjoiZXhhbXBsZTEwQGFzZC5jb20iLCJyb2xlIjoiYWRtaW4iLCJwYXNzd29yZCI6ImFkbWluIn0.52A-HsBOMLwRcpSWdHGBBo6-PYW32WnbPMwKkfLnCOU
```
Shows all courses with all details if the admin is logged in.


!FUNCTION INSTRUCTIONS TO BE FINISHED!

