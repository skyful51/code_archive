import requests
import time

url = "http://localhost:80/actuator/health"  # 실제 서버 URL로 변경해주세요.

def send_request():
    try:
        response = requests.get(url)
        # 응답 코드와 내용을 출력
        print(f"Response Code: {response.status_code}")
        print(f"Response Content: {response.text}")
    except requests.RequestException as e:
        print(f"Request Exception: {e}")

if __name__ == "__main__":
    # 10번의 요청을 보냅니다. (총 5초 동안)
    for _ in range(100):
        send_request()
        time.sleep(0.5)