from fastapi import FastAPI

from routers import tasks, projects, users, comments

app = FastAPI()

app.include_router(tasks.router)
app.include_router(projects.router)
app.include_router(users.router)
app.include_router(comments.router)

