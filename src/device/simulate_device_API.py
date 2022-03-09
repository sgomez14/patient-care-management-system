import device
import json
import requests

# BASE = "http://127.0.0.1:5000/"
BASE = "http://device-api.us-east-1.elasticbeanstalk.com/"

def simulate_send_measurements(json_file: str):  # -> List[bool, str]

    results = device.send_measurements(json_file)

    return results


def simulate_validate_JSON(json_file: str):  # -> List[bool, str]

    results = device.validate_JSON(json_file)

    return results


def rest_api_validate(file):
    print("URL invoked for validation: " + BASE + "device/validate/" + file)

    response = requests.get(BASE + "device/validate/" + file)

    print(response.status_code)

    if response.ok:
        json_response = json.dumps(response.json(), indent=4)
    else:
        json_response = "error with request"

    print(json_response)


def rest_api_send_measurements(file):
    print("URL invoked for sending measurement: " + BASE + "device/send-measurements/" + file)

    response = requests.post(BASE + "device/send-measurements/" + file)

    print(response.status_code)

    if response.ok:
        json_response = json.dumps(response.json(), indent=4)
    else:
        json_response = "error with request"

    print(json_response)


if __name__ == '__main__':
    file1 = "data/tempJSON.json"
    file2 = "data/temp_bp.json"
    files = ["tempJSON.json", "temp_bp.json"]
    database_file = "data/database.json"
    databaseData = ""

    # open json file
    opening_results = device._open_json(file2)

    # convert to json string
    inputData = json.dumps(opening_results[2])

    # call validate API by passing json string
    results = simulate_validate_JSON(inputData)

    print(results)

    # call REST APIs
    rest_api_validate(inputData)
    rest_api_send_measurements(inputData)


