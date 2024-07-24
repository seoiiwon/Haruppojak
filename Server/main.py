from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
from api import AuthRouter, CalendarRouter, MainRouter, DiaryRouter, ProfileRouter
from models import TodoListModel
from schemas import TodoListSchema
from crud import MainCrud
app = FastAPI()

# app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router.router)
