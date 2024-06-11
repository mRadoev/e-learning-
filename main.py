from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from routers.users import users_router
from routers.courses import courses_router
from routers.sections import sections_router
from fastapi.templating import Jinja2Templates
import uvicorn


app = FastAPI()
app.include_router(users_router)
app.include_router(courses_router)
app.include_router(sections_router)

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    # Render the HTML template
    return templates.TemplateResponse("index.html", {"request": request})


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
