import requests
import json

data={
    "action": "start_all"
} 

# 发送 POST 请求
# url = 'http://192.168.3.4:8080/receive_json'  # 服务器端接收 JSON 数据的 URL
url = 'http://192.168.3.4:8080/start_task_queue'
headers = {'Content-Type': 'application/json'}
response = requests.post(url, data=json.dumps(data), headers=headers)

# 打印响应内容
print(response.text)