import requests
import json

from src.chat.chat import ChatDB
from src.chat.chat_utils import *


# BASE = "http://patient-care-system-api.us-east-1.elasticbeanstalk.com/"
BASE = " http://127.0.0.1:5000/"


def validate_chat_packet(chat_packet: dict):

    chat_string = json.dumps(chat_packet)
    print("URL invoked for chat validation: " + BASE + "chat/validate-chat-packet/" + chat_string)

    response = requests.get(BASE + "chat/validate-chat-packet/" + chat_string)

    print(response.status_code)

    if response.ok:
        json_response = response.text  # json.dumps(response.json(), indent=4)
    else:
        json_response = response.text

    print(json_response)


if __name__ == '__main__':

    print(validate_chat_packet(chat_json_example))
    print(ChatDB.find_by_message_id(1234))

    print()
