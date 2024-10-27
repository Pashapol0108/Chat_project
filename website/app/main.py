from fastapi import FastAPI, Depends, Request, Form, HTTPException, status, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
import crud, models, db, auth
from schemas import UserCreate, ChatRoomCreate
from config import ACCESS_TOKEN_EXPIRE_MINUTES
from auth import create_access_token, verify_password, get_current_user
from datetime import timedelta
from db import get_db


#docker-compose up

app = FastAPI()

# Настройка Jinja2
templates = Jinja2Templates(directory="/app/templates")

models.Base.metadata.create_all(bind=db.engine)

def get_db():
    db_session = db.SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return RedirectResponse(url="/login/")

@app.get("/register/", response_class=HTMLResponse)
def show_register_form(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@app.post("/register/")
def register_user(email: str = Form(...), password: str = Form(...), nickname: str = Form(...), db: Session = Depends(get_db)):
    existing_user = crud.get_user_by_email(db, email=email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким email уже существует"
        )
    user_in_db = crud.create_user(db=db, email=email, password=password, nickname=nickname)
    return RedirectResponse(url="/login/", status_code=302)


@app.get("/login/", response_class=HTMLResponse)
def show_login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/logout/")
def logout(response: Response):
    return RedirectResponse(url="/login/", status_code=302)

@app.post("/token", response_class=HTMLResponse)
def login_for_access_token(request: Request, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, email=form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Устанавливаем срок действия токена
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)

    # Перенаправляем пользователя в комнаты и устанавливаем куки с токеном
    response = RedirectResponse(url="/chatrooms/", status_code=302)
    response.set_cookie(key="Authorization", value=f"Bearer {access_token}", httponly=True)

    return response


from fastapi import Response  # Не забудьте импортировать Response

@app.get("/chatrooms/", response_class=HTMLResponse)
def get_chatrooms(request: Request, response: Response, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):

    if isinstance(user, RedirectResponse):
        return user

    chatrooms = crud.get_chatrooms(db, search="")
    my_chatrooms = [room for room in chatrooms if room.owner_id == user.id]
    other_chatrooms = [room for room in chatrooms if room.owner_id != user.id]

    token = request.cookies.get("Authorization")  # Получение токена из куки

    return templates.TemplateResponse("chatrooms.html", {
        "request": request,
        "my_chatrooms": my_chatrooms,
        "other_chatrooms": other_chatrooms,
        "token": token[7:],  # Убираем "Bearer "
        "user": user
    })




@app.post("/chatrooms/")
async def create_chatroom(request: Request, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    form_data = await request.form()
    name = form_data.get("name")

    if not name:
        raise HTTPException(status_code=400, detail="Room name is required")

    chatroom = crud.create_chatroom(db=db, name=name, owner_id=user.id)

    return RedirectResponse(url="/chatrooms/", status_code=302)


@app.post("/chatrooms/delete/{room_id}")
async def delete_chatroom(room_id: int, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    chatroom = crud.get_chatroom_by_id(db, room_id)

    if chatroom is None:
        raise HTTPException(status_code=404, detail="Chatroom not found")

    if chatroom.owner_id != user.id:
        raise HTTPException(status_code=403, detail="You are not the owner of this chatroom")

    crud.delete_chatroom(db, room_id)

    return RedirectResponse(url="/chatrooms/", status_code=302)


@app.get("/chat/{room_name}", response_class=HTMLResponse)
def chat_room(request: Request, room_name: str, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    token = request.cookies.get("Authorization")[7:]  # Убираем "Bearer "
    return templates.TemplateResponse("chat.html", {
        "request": request,
        "room_name": room_name,
        "token": token,
        "user": user
    })

@app.post("/update_nickname/")
async def update_nickname(nickname: str = Form(...), db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    if not nickname:
        raise HTTPException(status_code=400, detail="Nickname is required")

    # Получаем актуального пользователя из базы данных для обновления
    user_in_db = db.query(models.User).filter(models.User.id == user.id).first()

    if user_in_db:
        user_in_db.nickname = nickname
        db.commit()   # Фиксируем изменения в базе данных
        db.refresh(user_in_db)  # Обновляем объект пользователя после сохранения

    return RedirectResponse(url="/chatrooms/", status_code=302)

@app.get("/search/")
def search_chats(query: str, db: Session = Depends(get_db)):
    chats = db.query(models.ChatRoom).filter(models.ChatRoom.name.ilike(f"%{query}%")).all()
    if not chats:
        raise HTTPException(status_code=404, detail="No chats found")
    return chats

