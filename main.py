from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
from Server.api.AuthRouter import auth_router

from Server.api.AuthRouter import DiaryRouter
from Server.api.MainRouter import Main_router

app = FastAPI()

app.mount("/static", StaticFiles(directory="Web/static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(DiaryRouter)
app.include_router(Main_router)
