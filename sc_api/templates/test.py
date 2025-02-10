import requests
import json

url1 = "http://127.0.0.1:8000/api/new_task"
headers = {'Content-Type': 'application/json'}
data1 = {
        "userID": "1",
        "start_time": "2024-01-20 12:11",
        "end_time": "2024-01-20 23:24",
        "name": "Run it back",
        "type": "W",
    }

response1 = requests.post(url1, headers=headers, data=json.dumps(data1))

print(f"Status Code: {response1.status_code}")
with(open("response1.html", "w") as f):
    f.write(response1.text)