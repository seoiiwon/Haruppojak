from fastapi import APIRouter, Depends, Query, Request, status, HTTPException, Form
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from Server.config.database import get_db
from Server.crud.ChallengeCrud import joinedChallenge, joinedChallengeID
from Server.crud.TokenForAuth import getCurrentUser
from Server.models.TodoListModel import *
from Server.schemas.TodoListSchema import *
from Server.crud.MainCrud import *
from Server.schemas import AuthSchema
from Server.crud.ChallengeCrud import joinedChallengeID, joinedChallenge
import os

router = APIRouter()

template_dir = os.path.join(os.path.dirname(
    __file__), "../../Web/templates/MainPage")
templates = Jinja2Templates(directory=template_dir)

template_dir_auth = os.path.join(os.path.dirname(
    __file__), "../../Web/templates/AuthPage")

templates_auth = Jinja2Templates(directory=template_dir_auth)

template_dir_auth = os.path.join(os.path.dirname(
    __file__), "../../Web/templates/AuthPage")

templates_auth = Jinja2Templates(directory=template_dir_auth)


# 투두리스트 보기
@router.get("/haru/main", response_class=HTMLResponse)
async def read_todos(request: Request, date: Optional[str] = Query(None), db: Session = Depends(get_db), currentUser: AuthSchema.UserInfoSchema = Depends(getCurrentUser)):

    token = request.cookies.get("access_token")
    if token:
        joinedChallengeIDList = joinedChallengeID(currentUser.id, db)
        joinedChallenges = joinedChallenge(joinedChallengeIDList, db)
        # 일기 작성은 True, 작성 안하면 False
        writtentoday = checkdiary(db, currentUser.id)
        if date:
            try:
                target_date = datetime.strptime(date, '%Y-%m-%d').date()
            except ValueError:
                raise HTTPException(
                    status_code=400, detail="잘못된 날짜 형식입니다.")
            todos = get_todos_by_date(db, currentUser.id, target_date)
        else:
            todos = get_todos(db, currentUser.id)
        return templates.TemplateResponse(name="mainPage.html", context={"request": request, "todos": todos, "joinedChallenge": joinedChallenges, "writtentoday": writtentoday})
    else:
        return templates_auth.TemplateResponse(name="HaruPpojakSignIn.html", request=request)


# todo 만들기
@router.post("/todo/create", response_model=TodoListSchema.TodoCreate)
async def create_new_todo(
    todo: TodoListSchema.TodoCreate, db: Session = Depends(get_db)
):
    return create_todo(db=db, todo=todo)


# todo 수정하기
# @router.put("/todo/update/{todo_id}", response_model=TodoListSchema.TodoUpdate)
# async def update_new_todo(
#     todo_id: int, todo: TodoListSchema.TodoUpdate, db: Session = Depends(get_db)
# ):
#     return update_todo(db=db, todo_id=todo_id, todo_update=todo)

# todo 수정하기


@router.put("/todo/update/{todo_id}", response_model=TodoListSchema.TodoUpdate)
async def update_new_todo(
    todo_id: int,
    todo: TodoListSchema.TodoUpdate,
    currentUser: AuthSchema.UserInfoSchema = Depends(getCurrentUser),
    db: Session = Depends(get_db),
):
    updated_todo = update_todo(
        db=db, todo_id=todo_id, todo_update=todo, user_id=currentUser.id)
    if updated_todo:
        return JSONResponse(content={"success": True, "todo": updated_todo.todo})
    else:
        raise HTTPException(status_code=404, detail="Todo not found")


# todo 삭제하기
@router.delete("/todo/delete/{todo_id}", response_model=None)
async def delete_existing_todo(
    todo_id: int, db: Session = Depends(get_db), currentUser: AuthSchema.UserInfoSchema = Depends(getCurrentUser)
):
    deleted_todo = delete_todo(db=db, todo_id=todo_id, user_id=currentUser.id)
    if deleted_todo:
        return JSONResponse(content={"success": True})
    else:
        raise HTTPException(status_code=404, detail="Todo not found")


# todo 체크
@router.put("/todo/check/{todo_id}", response_model=TodoListSchema.TodoCheck)
async def check_existing_todo(
    todo_id: int, todo: TodoListSchema.TodoCheck, db: Session = Depends(get_db)
):
    return check_todo(db=db, todo_id=todo_id, todo_check=todo)


# 추천 todo리스트
@router.get("/todo/recommendations", response_model=TopTodoRecommendations)
async def get_recommended_todos(db: Session = Depends(get_db)):
    top_recommendations = get_recommended_todos(db)
    return {"recommendations": [item[0] for item in top_recommendations]}


Mainrouter = router
