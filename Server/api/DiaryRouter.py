from fastapi import APIRouter, Depends, Request, status, HTTPException, Form
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from crud import DiaryCrud
from schemas import DiarySchema
from config.database import get_db
import os

router = APIRouter()

template_dir = os.path.join(os.path.dirname(__file__), "../../Web/templates/AuthPage")
templates = Jinja2Templates(directory=template_dir)

<<<<<<< Updated upstream
@router.get("/diary/write", response_class=HTMLResponse)
async def diarywritehtml(request : Request):
    return templates.TemplateResponse(name="writeDiary.html", request=request)

@router.post("/diary/write", status_code=status.HTTP_204_NO_CONTENT)
async def creatediarys(creatediarys : DiarySchema.CreateDiarySchema, db : Session=Depends(get_db)):
    DiaryCrud.CreateDiary(db=db, diary=creatediarys)
=======
# @router.get("diary/write", response_class=HTMLResponse)
# async def diarywritehtml(request : Request):
#     return HTMLResponse(name="diary.html",request = request)

# @router.post("/diary/write", status_code=status.HTTP_204_NO_CONTENT)
# async def creatediarys(creatediarys : schemas.CreateDiarySchema, db : Session=Depends(get_db)):
#     crud.CreateDiary(db=db, diary=creatediarys)

@router.post("/diary/write", status_code=status.HTTP_201_CREATED)
async def creatediarys(creatediarys: DiarySchema.CreateDiarySchema, db: Session = Depends(get_db)):
    new_diary = DiaryCrud.CreateDiary(db=db, diary=creatediarys)
    return JSONResponse(content=new_diary, status_code=status.HTTP_201_CREATED)
>>>>>>> Stashed changes

DiaryRouter = router