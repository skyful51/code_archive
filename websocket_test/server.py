from fastapi import FastAPI, WebSocket, Request
from fastapi.responses import HTMLResponse

import cv2
import numpy as np
import base64

from time import perf_counter
from datetime import datetime
import sys
import json

from loguru import logger
logger.add("file.log", format="{message}", level="INFO")
logger.info(f"client_time, server_time, host_ip, frame_id")

html = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>WebCam Streaming</title>
</head>
<body>

<video id="webcam" width="640" height="480" autoplay></video>
<button id="startBtn">Start</button>
<button id="endBtn">End</button>

<script>
var count = 0;
document.addEventListener('DOMContentLoaded', () => {
  const webcam = document.getElementById('webcam');
  const startBtn = document.getElementById('startBtn');
  const endBtn = document.getElementById('endBtn');
  let isStreaming = false;

  // 웹캠 스트림 가져오기
navigator.mediaDevices.getUserMedia({ video: { width: 1920, height: 1080 } })
    .then((stream) => {
        webcam.srcObject = stream;
    })
    .catch((error) => {
        console.error('Error accessing webcam:', error);
    });

  // WebSocket 연결
  const socket = new WebSocket('ws://161.122.115.215:8000/ws');

  // start 버튼 클릭 시 이미지 전송 시작
  startBtn.addEventListener('click', () => {
    if (!isStreaming) {
      isStreaming = true;
      sendWebcamImage();
    }
  });

  // end 버튼 클릭 시 이미지 전송 중지
  endBtn.addEventListener('click', () => {
    if (isStreaming) {
      isStreaming = false;
    }
  });

    // 현재 시간을 문자열로 반환하는 함수
  function getCurrentTimestamp() {
    const date = new Date();
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    const seconds = String(date.getSeconds()).padStart(2, '0');
    const milliseconds = String(date.getMilliseconds());
    return `${hours}:${minutes}:${seconds}.${milliseconds}`;
  }
  
  // 이미지를 주기적으로 전송하는 함수
  function sendWebcamImage() {
    if (isStreaming) {
      const canvas = document.createElement('canvas');
      canvas.width = webcam.videoWidth;
      canvas.height = webcam.videoHeight;
      const ctx = canvas.getContext('2d');
      ctx.drawImage(webcam, 0, 0, canvas.width, canvas.height);

      const imageData = canvas.toDataURL('image/jpeg', 1);
      const data = JSON.stringify({image: imageData, timestamp: getCurrentTimestamp(), frame_id: count++});
      socket.send(data);

      // 주기적으로 이미지 전송 (1초마다)
      setTimeout(sendWebcamImage, 100);
    }
  }
});
</script>

</body>
</html>
"""

app = FastAPI()

@app.get("/")
async def get():
    return HTMLResponse(html)

@app.websocket("/ws")
async def websocket_endpoint(request: Request, websocket: WebSocket):
    await websocket.accept()
    host_ip = request.client.host
    while True:
        data = await websocket.receive_text()
        server_timestamp = datetime.now().time().strftime("%H:%M:%S.%f")[:-3]
        data_dict = json.loads(data)
        image_data = data_dict['image']
        client_timestamp = data_dict['timestamp']
        frame_id = data_dict['frame_id']
        img_base64 = image_data[image_data.find('base64,') + 7:]
        imgdata = base64.b64decode(img_base64)
        np_data = np.frombuffer(imgdata, np.uint8)
        img0 = cv2.imdecode(np_data, cv2.IMREAD_UNCHANGED)
        logger.info(f"image shape: {img0.shape[:2]}, data size: {sys.getsizeof(image_data) // 1024} kB")
        await websocket.send_text(f"image shape: {img0.shape[:2]}")
        print(f"client: {client_timestamp}, server: {server_timestamp}")
        logger.info(f"{client_timestamp}, {server_timestamp}, {host_ip}, {frame_id}")

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')