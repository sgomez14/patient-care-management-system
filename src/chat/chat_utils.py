import json
import logging
import enum
import requests


class ApiResult(enum.Enum):
    """This class enumerated codes to indicate the result of an API call."""

    SUCCESS = 200
    DEFAULT_FAIL = 400
    NOT_FOUND = 404
    CONFLICT = 409


def dump_into_json_string(data: dict):
    """This function dumps dictionary into a JSON string"""

    # helper code from Kite.com
    # https://www.kite.com/python/answers/how-to-handle-json-decode-error-when-nothing-returns-in-python

    try:
        data = json.dumps(data)
        msg = f"Dumping into JSON string: Successfully created JSON string: {data}"
        logging.info(msg)
        return [True, msg, ApiResult.SUCCESS.value, data]

    except json.decoder.JSONDecodeError:
        data = {}
        msg = "Dumping JSON string: JSON string could not be created."
        logging.error(msg)
        return [False, msg, ApiResult.CONFLICT.value, data]



def load_json_string(json_string: str):  # -> List[bool, str, ApiResult, json object]
    """This function loads json from a string"""

    # helper code from Kite.com
    # https://www.kite.com/python/answers/how-to-handle-json-decode-error-when-nothing-returns-in-python

    try:
        data = json.loads(json_string)
        msg = f"Loading JSON string: Successfully loaded JSON string called: {json_string}"
        logging.info(msg)
        return [True, msg, data, ApiResult.SUCCESS.value]

    except json.decoder.JSONDecodeError as err:
        data = {}
        msg = "Loading JSON string: JSON String could not be converted."
        logging.error(msg)
        logging.error(f"Loading JSON string: JSON exception -> {err}")
        return [False, msg, data, ApiResult.CONFLICT.value]


chat_schema = {
    "$schema": "http://json-schema.org/draft-06/schema#",
    "$ref": "#/definitions/Chat",
    "definitions": {
        "Chat": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "api_access_token": {
                    "type": "integer"
                },
                "message_packet": {
                    "type": "array",
                    "items": {
                        "$ref": "#/definitions/MessagePacket"
                    }
                }
            },
            "required": [
                "api_access_token",
                "message_packet"
            ],
            "title": "Chat"
        },
        "MessagePacket": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "message_id": {
                    "type": "integer"
                },
                "session_id": {
                    "type": "integer"
                },
                "timestamp": {
                    "type": "string",
                    "format": "date-time"
                },
                "device": {
                    "type": "string"
                },
                "sender": {
                    "$ref": "#/definitions/Sender"
                },
                "recipients": {
                    "type": "array",
                    "items": {
                        "$ref": "#/definitions/Sender"
                    }
                },
                "text": {
                    "type": "string"
                },
                "attachments": {
                    "$ref": "#/definitions/Attachments"
                }
            },
            "required": [
                "attachments",
                "device",
                "message_id",
                "recipients",
                "sender",
                "session_id",
                "text",
                "timestamp"
            ],
            "title": "MessagePacket"
        },
        "Attachments": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "media": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    }
                },
                "voice": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    }
                },
                "files": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    }
                }
            },
            "required": [
                "files",
                "media",
                "voice"
            ],
            "title": "Attachments"
        },
        "Sender": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "user": {
                    "$ref": "#/definitions/User"
                }
            },
            "required": [
                "user"
            ],
            "title": "Sender"
        },
        "User": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "username": {
                    "type": "string"
                },
                "user_id": {
                    "type": "integer"
                },
                "first_name": {
                    "type": "string"
                },
                "last_name": {
                    "type": "string"
                }
            },
            "required": [
                "first_name",
                "last_name",
                "user_id",
                "username"
            ],
            "title": "User"
        }
    }
}

chat_json_wrong = {}

chat_json_example = {
    "api_access_token": 4567,
    "message_packet": [
        {
            "message_id": 1234,
            "session_id": 9876,
            "timestamp": "2022-03-12T17:45:07",
            "device": "iOS",
            "sender": {"user": {"username": "user1", "user_id": 4321, "first_name": "santiago", "last_name": "gomez"}},
            "recipients":
                [
                    {"user": {"username": "user2", "user_id": 4322, "first_name": "ben", "last_name": "kuter"}},
                    {"user": {"username": "user3", "user_id": 4323, "first_name": "mandy", "last_name": "yao"}}
                ],
            "text": "this is the message user1 sent to user2 and user3",
            "attachments":
                {
                    "media": ["photos.com/photo1", "videos.com/vid1"],
                    "voice": ["voice-memo.com/memo1"],
                    "files": ["files.com/file1"]
                }
        },

        {
            "message_id": 1235,
            "session_id": 9877,
            "timestamp": "2022-03-12T18:45:07",
            "device": "android",
            "sender": {"user": {"username": "user2", "user_id": 4322, "first_name": "ben", "last_name": "kuter"}},
            "recipients":
                [
                    {"user": {"username": "user1", "user_id": 4321, "first_name": "santiago", "last_name": "gomez"}}
                ],
            "text": "this is the message user2 sent to user1",
            "attachments":
                {
                    "media": ["photos.com/photo2"],
                    "voice": [],
                    "files": []
                }
        }
    ]
}

chat_json_example2 = {
    "api_access_token": 4567,
    "message_packet": [

        {
            "message_id": 1239,
            "session_id": 9877,
            "timestamp": "2022-03-12T18:45:07",
            "device": "android",
            "sender": {"user": {"username": "user2", "user_id": 4322, "first_name": "ben", "last_name": "kuter"}},
            "recipients":
                [
                    {"user": {"username": "user1", "user_id": 4321, "first_name": "santiago", "last_name": "gomez"}}
                ],
            "text": "this is the message user2 sent to user1",
            "attachments":
                {
                    "media": ["photos.com/photo2"],
                    "voice": [],
                    "files": []
                }
        }
    ]
}

mongo_chat_document1 = {
    "message_id": 1235,
    "session_id": 9877,
    "timestamp": "2022-03-12T18:45:07",
    "device": "android",
    "sender": {"user": {"username": "user2", "user_id": 4322, "first_name": "ben", "last_name": "kuter"}},
    "recipients":
        [
            {"user": {"username": "user1", "user_id": 4321, "first_name": "santiago", "last_name": "gomez"}}
        ],
    "text": "this is the message user2 sent to user1",
    "attachments":
        {
            "media": ["photos.com/photo2"],
            "voice": [],
            "files": []
        },
    "message_owner": 4567
}

mongodb_pwd = "WgAVFP22prU8sVHW"
mongodb_user = "sgomez22"
mongodb_cluster = "PCMS-Database"


# testing purposes only
BASE = "http://patient-care-system-api.us-east-1.elasticbeanstalk.com/"


def validate_chat_packet_api_call(chat_packet: dict):

    chat_string = json.dumps({
    "api_access_token": 4567,
    "message_packet": [
        {
            "message_id": 1234,
            "session_id": 9876,
            "timestamp": "2022-03-12T17:45:07",
            "device": "iOS",
            "sender": {"user": {"username": "user1", "user_id": 4321, "first_name": "santiago", "last_name": "gomez"}},
            "recipients":
                [
                    {"user": {"username": "user2", "user_id": 4322, "first_name": "ben", "last_name": "kuter"}},
                    {"user": {"username": "user3", "user_id": 4323, "first_name": "mandy", "last_name": "yao"}}
                ],
            "text": "this is the message user1 sent to user2 and user3",
            "attachments":
                {
                    "media": ["photos.com/photo1", "videos.com/vid1"],
                    "voice": ["voice-memo.com/memo1"],
                    "files": ["files.com/file1"]
                }
        }]})

    print(chat_string)
    # print("URL invoked for chat validation: " + BASE + f"chat/validate-chat-packet/{chat_string}")
    print(type(chat_string))
    # chat_string = '{"api_access_token": 4567, "message_packet":hi}'


    response = requests.get(f"http://patient-care-system-api.us-east-1.elasticbeanstalk.com/chat/validate-chat-packet/{chat_packet}")

    print(response.status_code)
    print(response.url)

    if response.ok:
        json_response = response.text  # json.dumps(response.json(), indent=4)
    else:
        json_response = response.text

    print(json_response)


if __name__ == '__main__':

    # chat_packet = json.dumps(chat_json_example)
    # print(type(chat_json_example))
    # print(validate_chat_packet_api_call(chat_json_example))

    url = "http://patient-care-system-api.us-east-1.elasticbeanstalk.com/chat/"

    url += 'get-chat-by-message-id/{"api_access_token": 4567, "message_id": 1234}'

    response = requests.request("GET", url)

    print(response.text)

    # url += 'get-chat-by-session-id/{"api_access_token": 4567, "session_id": 9876}'
    # url += 'get-chat-by-message-owner/{"api_access_token": 4567, "message_owner": 4567}'
    #

    #
    #
    # chat_packet = json.dumps({"homer": 12345, "homer1": 12345, "homer3": 12345})
    #
    # response = requests.get(
    #     f"http://patient-care-system-api.us-east-1.elasticbeanstalk.com/chat/validate-chat-packet/{chat_packet}")
    #
    # print(response.status_code)
    # print(response.url)
    #
    # if response.ok:
    #     json_response = response.text  # json.dumps(response.json(), indent=4)
    # else:
    #     json_response = response.text
    #
    # print(json_response)

    # url = "http://patient-care-system-api.us-east-1.elasticbeanstalk.com/chat/store-chat"
    #
    # chat_packet = json.dumps(chat_json_example2)
    # # url += f"{chat_packet}"
    #
    # response = requests.post(url + '/{"hello": 1}')
    #
    # print(response.status_code)
    # print(response.url)
    #
    # if response.ok:
    #     json_response = response.text  # json.dumps(response.json(), indent=4)
    # else:
    #     json_response = response.text
    #
    # print(json_response)



