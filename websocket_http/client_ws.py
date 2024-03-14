import cv2
import base64
import asyncio
import websockets

# Set the video capture device (0 for default webcam)
cap = cv2.VideoCapture(0)

# Set the video resolution to 1920x1080
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

# WebSockets server URL
url = "ws://127.0.0.1:8000/ws"

async def send_frame():
    async with websockets.connect(url) as websocket:

        while True:
            # Capture frame-by-frame
            ret, frame = cap.read()

            # Check if frame is captured successfully
            if not ret:
                continue

            # Convert the frame to JPEG format
            _, img_encoded = cv2.imencode('.jpg', frame)
            img_bytes = img_encoded.tobytes()
            img_base64 = base64.b64encode(img_bytes)

            # Send the frame to the WebSockets server
            await websocket.send(img_base64)

            print(f"{len(img_base64) / 1024} kB")

            await asyncio.sleep(0.1)

asyncio.get_event_loop().run_until_complete(send_frame())