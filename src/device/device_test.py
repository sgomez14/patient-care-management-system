import device
import json


def test_send_measurements_temp_json_file() -> None:
    """Tests that JSON containing only temperature data has all correct keys"""

    input_file = "data/tempJSON.json"

    results = device.send_measurements(input_file, True)

    API_success: bool = results[0]

    assert API_success


def test_validate_temp_json_file() -> None:
    """Tests validate API call that JSON containing only temperature data has all correct keys and value types"""

    input_file = "data/tempJSON.json"

    results = device.validate_JSON(input_file, True)

    API_success: bool = results[0]

    assert API_success


def test_validate_temp_bp_json_file() -> None:
    """Tests validate API call that JSON containing temperature and blood pressure data has all correct keys"""

    input_file = "data/temp_bp.json"

    results = device.validate_JSON(input_file, True)

    API_success: bool = results[0]

    assert API_success


def test_empty_json_file_file() -> None:
    """Test validate API call for an empty JSON file"""

    input_file = "data/emptyFile.json"

    results = device.validate_JSON(input_file, True)

    API_success: bool = results[0]

    assert not API_success


def test_validate_json_string() -> None:
    """Test validate API call when sending a JSON string"""

    files = ["data/tempJSON.json", "data/temp_bp.json"]
    results = []

    for file in files:
        # open a json file stored in data directory
        opening_results = device.open_json(file)

        # convert json object to json string
        inputData = json.dumps(opening_results[2])

        # call validate function and pass a json string
        validate_results = device.validate_JSON(inputData)

        # append validate_results to results list
        results.append(validate_results[0])

    API_success: bool = all(results)

    assert API_success


def test_validate_empty_json_string() -> None:
    """Test validate API call when sending an empty JSON string"""

    json_string = "{}"

