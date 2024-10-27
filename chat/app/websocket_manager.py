from typing import List, Dict
from fastapi import WebSocket

class WebSocketManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, chatroom_name: str):
        await websocket.accept()
        if chatroom_name not in self.active_connections:
            self.active_connections[chatroom_name] = []
        self.active_connections[chatroom_name].append(websocket)

    def disconnect(self, websocket: WebSocket, chatroom_name: str):
        self.active_connections[chatroom_name].remove(websocket)

    async def broadcast(self, message: str, chatroom_name: str):
        for connection in self.active_connections.get(chatroom_name, []):
            await connection.send_text(message)
