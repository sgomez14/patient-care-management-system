import json

devices: dict = {"device_ids": [9876, 1000, 123]}


def get_json_registered_devices():

    json_string = json.dumps(devices, indent=4)
    return json_string
