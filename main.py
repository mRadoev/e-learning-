from fastapi import FastAPI
from routers.users import users_router
from routers.courses import courses_router
from routers.sections import sections_router
from fastapi.templating import Jinja2Templates
import uvicorn


app = FastAPI()
app.include_router(users_router)
app.include_router(courses_router)
app.include_router(sections_router)

templates = Jinja2Templates(directory="templates")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)