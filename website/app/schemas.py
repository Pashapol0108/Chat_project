from pydantic import BaseModel

class UserCreate(BaseModel):
    email: str
    password: str

class ChatRoomCreate(BaseModel):
    name: str
    owner_id: int