import cv2
import base64
import json
import requests
import time
import sys

# Set the video capture device (0 for default webcam)
cap = cv2.VideoCapture(0)

# Set the video resolution to 1920x1080
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

# HTTP server URL
url = "http://127.0.0.1:8000/http"

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Check if frame is captured successfully
    if not ret:
        continue

    # Convert the frame to JPEG format
    _, img_encoded = cv2.imencode('.jpg', frame)
    img_base64 = base64.b64encode(img_encoded.tobytes())
    img_base64 = img_base64.decode('utf-8')
    req_data = json.dumps({'data': img_base64})

    # Send the frame to the HTTP server
    response = requests.post(url, data=req_data)
    # Check the response status
    if response.status_code != 200:
        print("Failed to send frame to the server")

    print(f"{sys.getsizeof(img_base64) / 1024} kB")

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    time.sleep(0.1)

# Release the video capture device and close the window
cap.release()