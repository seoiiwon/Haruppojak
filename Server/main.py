from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
<<<<<<< Updated upstream:Server/main.py
from api import AuthRouter, CalendarRouter, MainRouter, DiaryRouter, ProfileRouter
from models import TodoListModel
from schemas import TodoListSchema
from crud import MainCrud
=======
from Server.api.AuthRouter import auth_router
from Server.api.MainRouter import Main_router
>>>>>>> Stashed changes:main.py
app = FastAPI()

# app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

<<<<<<< Updated upstream:Server/main.py
app.include_router(router.router)
=======
app.include_router(auth_router)
app.include_router(Main_router)
>>>>>>> Stashed changes:main.py
