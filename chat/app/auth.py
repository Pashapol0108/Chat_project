from jose import JWTError, jwt
from fastapi import HTTPException, status
from config import SECRET_KEY, ALGORITHM
from sqlalchemy.orm import Session
import models

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_current_user(token: str, db: Session):
    print(f"Checking token: {token}")  # Отладочный вывод токена

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if token.startswith("Bearer "):
        token = token[7:]

    credentials_exception = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_email: str = payload.get("sub")
        if user_email is None:
            raise credentials_exception
    except JWTError as e:
        print(f"JWT error: {e}")  # Вывод ошибки JWT
        raise credentials_exception

    # Получаем пользователя из базы данных по email
    user = get_user_by_email(db, email=user_email)
    if user is None:
        raise credentials_exception

    return user  # Возвращаем объект пользователя с никнеймом
