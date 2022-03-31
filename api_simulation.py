import requests
import json

BASE = "http://127.0.0.1:5000/"

jsonS = {'api_access_token': 4567, 'message_id': 1235}
json_s = json.dumps(jsonS)

response = requests.get(BASE + "chat/get-chat-by-message-id/" + json_s)
print(response.json())