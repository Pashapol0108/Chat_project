from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Query, Depends, HTTPException
from sqlalchemy.orm import Session
from auth import get_current_user
from db import get_db
from typing import List, Dict

#uvicorn website.app.main:app --reload
#uvicorn chat.app.main:app --reload --port 8001

app = FastAPI()


# Класс для управления подключениями к WebSocket с разделением по чатам
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}  # Отдельные списки для каждого чата

    async def connect(self, websocket: WebSocket, room_name: str):
        await websocket.accept()
        if room_name not in self.active_connections:
            self.active_connections[room_name] = []
        self.active_connections[room_name].append(websocket)

    def disconnect(self, websocket: WebSocket, room_name: str):
        self.active_connections[room_name].remove(websocket)
        if len(self.active_connections[room_name]) == 0:
            del self.active_connections[room_name]

    async def broadcast(self, message: str, room_name: str):
        for connection in self.active_connections.get(room_name, []):
            await connection.send_text(message)

manager = ConnectionManager()

@app.get("/")
def read_root():
    return {"message": "Welcome to the WebSocket chat!"}

# WebSocket маршрут для подключения к чат-комнате
@app.websocket("/ws/chat/{room_name}")
async def websocket_chat(websocket: WebSocket, room_name: str, token: str = Query(None), db: Session = Depends(get_db)):
    print(f"Token received: {token}")
    try:
        if not token:
            # Закрываем соединение с кодом 4001 (например, пользователь не авторизован)
            await websocket.close(code=4001)
            print("Token not provided")
            return

        # Проверка JWT токена и получение пользователя
        user = get_current_user(token, db)
        await manager.connect(websocket, room_name)  # Привязываем соединение к конкретной комнате
        await manager.broadcast(f"{user.nickname} присоединился к чату {room_name}", room_name)  # Используем никнейм
        try:
            while True:
                data = await websocket.receive_text()
                await manager.broadcast(f"{user.nickname}: {data}", room_name)  # Используем никнейм при отправке сообщений
        except WebSocketDisconnect:
            manager.disconnect(websocket, room_name)
            await manager.broadcast(f"{user.nickname} покинул чат {room_name}", room_name)
    except Exception as e:
        print(f"Error occurred: {e}")
        await websocket.close(code=4002)
