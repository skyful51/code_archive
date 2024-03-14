from fastapi import FastAPI, WebSocket, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import sys

class Item(BaseModel):
    data: str

app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_bytes()
        print(f"{sys.getsizeof(data) / 1024} kB")

@app.post("/http")
async def receive_frame(item: Item):
    data = item.data
    # Process the image here
    return {"message": "Frame received and processed successfully"}

if __name__ == "__main__":
    app.run(debug=True)