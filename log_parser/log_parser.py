import csv
from datetime import datetime

log_file = "one_client_secure_wifi.log"
csv_file = "one_client_secure_wifi.csv"

with open(log_file, "r") as f:
    lines = f.readlines()

datas = []
for line in lines:
    data = []
    line = line.strip()
    parts = line.split(" - ")

    try:
        # 로그 공통 부분
        timestamp = parts[0].split(" | ")[0]
        date = timestamp.split(" ")[0]
        time = timestamp.split(" ")[1]
        info = parts[1].split(" ")
        event_type = info[0].strip("[]")
        ip = info[1].strip("[]")
        frame_id = info[2].strip("[]")

    except IndexError:
        continue

    # 로그 종류에 따른 처리
    if event_type == "REQUEST":
        decison_made = "N/A"
        time_elapsed = "N/A"
        client_timestamp = info[3].strip("[]")
        HH = int(client_timestamp.split(":")[0])
        MM = int(client_timestamp.split(":")[1])
        SS = int(client_timestamp.split(":")[2])
        mmm = int(client_timestamp.split(":")[3])
        client_timestamp = f"{HH}:{MM}:{SS}.{mmm}"
        data.append(event_type)
        data.append(date)
        data.append(time)
        data.append(client_timestamp)
        data.append(ip)
        data.append(frame_id)
        data.append(decison_made)
        data.append(time_elapsed)
    
    elif event_type == "RESPONSE":
        decision_made = info[3].strip("[]")
        time_elapsed = info[4].strip("[]")
        client_timestamp = "N/A"
        data.append(event_type)
        data.append(date)
        data.append(time)
        data.append(client_timestamp)
        data.append(ip)
        data.append(frame_id)
        data.append(decision_made)
        data.append(time_elapsed)

    elif event_type == "TASK":
        decision_made = info[4].strip("[]")
        time_elapsed = info[3].strip("[]")
        time_diff = "N/A"
        client_timestamp = "N/A"
        data.append(event_type)
        data.append(date)
        data.append(time)
        data.append(client_timestamp)
        data.append(ip)
        data.append(frame_id)
        data.append(decision_made)
        data.append(time_elapsed)
        
    print(data)
    datas.append(data)

with open(csv_file, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Event Type", "Date", "Time", "Client Time", "IP", "Frame ID", "Decision Made", "Duration"])
    writer.writerows(datas)
