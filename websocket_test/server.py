from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

import cv2
import numpy as np
import base64

from time import perf_counter
from datetime import datetime
import sys
import json

app = FastAPI()

@app.get("/")
async def get():
    return HTMLResponse("hello world")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        server_timestamp = datetime.now().time().strftime("%H:%M:%S.%f")[:-3]
        data_dict = json.loads(data)
        image_data = data_dict['image']
        timestamp = data_dict['timestamp']
        img_base64 = image_data[image_data.find('base64,') + 7:]
        imgdata = base64.b64decode(img_base64)
        np_data = np.frombuffer(imgdata, np.uint8)
        img0 = cv2.imdecode(np_data, cv2.IMREAD_UNCHANGED)
        print(f"image shape: {img0.shape[:2]}, data size: {sys.getsizeof(image_data) // 1024} kB")
        await websocket.send_text(f"image shape: {img0.shape[:2]}")
        print(f"client: {timestamp}, server: {server_timestamp}")

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')