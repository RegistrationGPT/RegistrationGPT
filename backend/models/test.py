import requests
import json

# 设置API的URL
url = "http://127.0.0.1:5000/python/api/process"

# 构建请求数据
conversation_history = [
    {"role": "user", "content": "Hello, World!"},
    {"role": "assistant", "content": "Hello! How can I assist you today?"},
    {"role": "user", "content": "I need to register for a pre-appointment."}
]

data = {
    "conversation_history": conversation_history
}

headers = {
    "Content-Type": "application/json"
}

# 发送POST请求以处理对话历史记录
response = requests.post(url, headers=headers, data=json.dumps(data))
print("Conversation History Processing Response:")
print("Status Code:", response.status_code)
print("Response JSON:", response.json())
