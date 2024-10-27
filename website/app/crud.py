from sqlalchemy.orm import Session
import models
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    return pwd_context.hash(password)


def create_user(db: Session, email: str, password: str, nickname: str):
    hashed_password = hash_password(password)
    user = models.User(email=email, hashed_password=hashed_password, nickname=nickname)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def create_chatroom(db: Session, name: str, owner_id: int):
    chatroom = models.ChatRoom(name=name, owner_id=owner_id)
    db.add(chatroom)
    db.commit()
    db.refresh(chatroom)
    return chatroom


def get_chatrooms(db: Session, search: str):
    return db.query(models.ChatRoom).filter(models.ChatRoom.name.contains(search)).all()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

# Получаем комнату по её id
def get_chatroom_by_id(db: Session, room_id: int):
    return db.query(models.ChatRoom).filter(models.ChatRoom.id == room_id).first()

# Функция для удаления комнаты
def delete_chatroom(db: Session, room_id: int):
    chatroom = get_chatroom_by_id(db, room_id)
    if chatroom:
        db.delete(chatroom)
        db.commit()
