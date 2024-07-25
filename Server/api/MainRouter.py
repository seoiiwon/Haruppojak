from fastapi import APIRouter, Depends, Request, status, HTTPException, Form
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
# from config.database import get_db
import os

router = APIRouter()

template_dir = os.path.join(os.path.dirname(
    __file__), "../../Web/templates/AuthPage")
templates = Jinja2Templates(directory=template_dir)

Main_router = router
