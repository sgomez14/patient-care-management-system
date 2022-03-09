import device
import json


def test_send_measurements_temp_json_file() -> None:
    """Tests that JSON containing only temperature data has all correct keys"""

    input_file = "data/tempJSON.json"

    results = device.send_measurements(input_file, passing_a_file=True)

    API_success: bool = results[0]

    assert API_success


def test_validate_temp_json_file() -> None:
    """Tests validate API call that JSON containing only temperature data has all correct keys and value types"""

    input_file = "data/tempJSON.json"

    results = device.validate_JSON(input_file, passing_a_file=True)

    API_success: bool = results[0]

    assert API_success


def test_validate_temp_bp_json_file() -> None:
    """Tests validate API call that JSON containing temperature and blood pressure data has all correct keys"""

    input_file = "data/temp_bp.json"

    results = device.validate_JSON(input_file, passing_a_file=True)

    API_success: bool = results[0]

    assert API_success


def test_empty_json_file() -> None:
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
        opening_results = device._open_json(file)

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

    results = device.validate_JSON(json_string)

    API_success: bool = results[0]

    assert not API_success


def test_validate_incorrect_timestamp() -> None:
    """Test validate API when timestamp is incorrect"""

    files = ["data/incorrect_timestamp.json"]
    results = []

    for file in files:
        # open a json file stored in data directory
        opening_results = device._open_json(file)

        # convert json object to json string
        inputData = json.dumps(opening_results[2])

        # call validate function and pass a json string
        validate_results = device.validate_JSON(inputData)

        # append validate_results to results list
        results.append(validate_results[0])

    API_success: bool = all(results)

    assert not API_success


def test_validate_missing_primary_keys() -> None:
    """Test validate API when primary keys are missing"""

    files = ["data/missing_primary_keys.json"]
    results = []

    for file in files:
        # open a json file stored in data directory
        opening_results = device._open_json(file)

        # convert json object to json string
        inputData = json.dumps(opening_results[2])

        # call validate function and pass a json string
        validate_results = device.validate_JSON(inputData)

        # append validate_results to results list
        results.append(validate_results[0])

    API_success: bool = all(results)

    assert not API_success


def test_validate_duplicate_primary_keys() -> None:
    """Test validate API when primary keys are duplicated"""

    files = ["data/duplicate_primary_keys.json"]
    results = []

    for file in files:
        # open a json file stored in data directory
        opening_results = device._open_json(file)

        # convert json object to json string
        inputData = json.dumps(opening_results[2])

        # call validate function and pass a json string
        validate_results = device.validate_JSON(inputData)

        # append validate_results to results list
        results.append(validate_results[0])

    API_success: bool = all(results)

    assert not API_success


def test_validate_incorrect_primary_keys() -> None:
    """Test validate API when primary keys are incorrect"""

    files = ["data/incorrect_primary_key.json"]
    results = []

    for file in files:
        # open a json file stored in data directory
        opening_results = device._open_json(file)

        # convert json object to json string
        inputData = json.dumps(opening_results[2])

        # call validate function and pass a json string
        validate_results = device.validate_JSON(inputData)

        # append validate_results to results list
        results.append(validate_results[0])

    API_success: bool = all(results)

    assert not API_success


def test_validate_incorrect_primary_keys_value() -> None:
    """Test validate API when primary keys values are not integers"""

    files = ["data/primary_key_value_not_int.json"]
    results = []

    for file in files:
        # open a json file stored in data directory
        opening_results = device._open_json(file)

        # convert json object to json string
        inputData = json.dumps(opening_results[2])

        # call validate function and pass a json string
        validate_results = device.validate_JSON(inputData)

        # append validate_results to results list
        results.append(validate_results[0])

    API_success: bool = all(results)

    assert not API_success


def test_validate_incorrect_primary_keys_value() -> None:
    """Test validate API when primary keys values are not integers"""

    files = ["data/primary_key_value_not_int.json"]
    results = []

    for file in files:
        # open a json file stored in data directory
        opening_results = device._open_json(file)

        # convert json object to json string
        inputData = json.dumps(opening_results[2])

        # call validate function and pass a json string
        validate_results = device.validate_JSON(inputData)

        # append validate_results to results list
        results.append(validate_results[0])

    API_success: bool = all(results)

    assert not API_success


def test_validate_primary_key_measure_value_not_dict() -> None:
    """Test validate API when primary keys measurement does not have a dictionary assigned to it"""

    files = ["data/primary_key_measure_value_not_dict.json"]
    results = []

    for file in files:
        # open a json file stored in data directory
        opening_results = device._open_json(file)

        # convert json object to json string
        inputData = json.dumps(opening_results[2])

        # call validate function and pass a json string
        validate_results = device.validate_JSON(inputData)

        # append validate_results to results list
        results.append(validate_results[0])

    API_success: bool = all(results)

    assert not API_success


def test_validate_primary_key_measure_empty_dict() -> None:
    """Test validate API when primary keys measurement has an empty dictionary assigned to it"""

    files = ["data/primary_key_measure_empty_dict.json"]
    results = []

    for file in files:
        # open a json file stored in data directory
        opening_results = device._open_json(file)

        # convert json object to json string
        inputData = json.dumps(opening_results[2])

        # call validate function and pass a json string
        validate_results = device.validate_JSON(inputData)

        # append validate_results to results list
        results.append(validate_results[0])

    API_success: bool = all(results)

    assert not API_success


def test_validate_invalid_measurement_key() -> None:
    """Test validate API when measurement key is invalid"""

    files = ["data/invalid_measurement_key.json"]
    results = []

    for file in files:
        # open a json file stored in data directory
        opening_results = device._open_json(file)

        # convert json object to json string
        inputData = json.dumps(opening_results[2])

        # call validate function and pass a json string
        validate_results = device.validate_JSON(inputData)

        # append validate_results to results list
        results.append(validate_results[0])

    API_success: bool = all(results)

    assert not API_success


def test_validate_measurement_key_value_not_list() -> None:
    """Test validate API when measurement key value is not a list"""

    files = ["data/measurement_key_value_not_list.json"]
    results = []

    for file in files:
        # open a json file stored in data directory
        opening_results = device._open_json(file)

        # convert json object to json string
        inputData = json.dumps(opening_results[2])

        # call validate function and pass a json string
        validate_results = device.validate_JSON(inputData)

        # append validate_results to results list
        results.append(validate_results[0])

    API_success: bool = all(results)

    assert not API_success


def test_validate_measurement_key_value_list_empty() -> None:
    """Test validate API when measurement key value is an empty list"""

    files = ["data/measurement_key_value_list_empty.json"]
    results = []

    for file in files:
        # open a json file stored in data directory
        opening_results = device._open_json(file)

        # convert json object to json string
        inputData = json.dumps(opening_results[2])

        # call validate function and pass a json string
        validate_results = device.validate_JSON(inputData)

        # append validate_results to results list
        results.append(validate_results[0])

    API_success: bool = all(results)

    assert not API_success


def test_validate_inner_data_incorrect_num_keys() -> None:
    """Test validate API when inner data has incorrect number of keys"""

    files = ["data/inner_data_incorrect_num_keys.json"]
    results = []

    for file in files:
        # open a json file stored in data directory
        opening_results = device._open_json(file)

        # convert json object to json string
        inputData = json.dumps(opening_results[2])

        # call validate function and pass a json string
        validate_results = device.validate_JSON(inputData)

        # append validate_results to results list
        results.append(validate_results[0])

    API_success: bool = all(results)

    assert not API_success


def test_validate_inner_data_incorrect_measurement_key() -> None:
    """Test validate API when inner data has missing measurement key"""

    files = ["data/inner_data_incorrect_measurement_key.json"]
    results = []

    for file in files:
        # open a json file stored in data directory
        opening_results = device._open_json(file)

        # convert json object to json string
        inputData = json.dumps(opening_results[2])

        # call validate function and pass a json string
        validate_results = device.validate_JSON(inputData)

        # append validate_results to results list
        results.append(validate_results[0])

    API_success: bool = all(results)

    assert not API_success


def test_validate_inner_data_incorrect_metadata_key() -> None:
    """Test validate API when inner data has incorrect unit key"""

    files = ["data/inner_data_incorrect_metadata_key.json"]
    results = []

    for file in files:
        # open a json file stored in data directory
        opening_results = device._open_json(file)

        # convert json object to json string
        inputData = json.dumps(opening_results[2])

        # call validate function and pass a json string
        validate_results = device.validate_JSON(inputData)

        # append validate_results to results list
        results.append(validate_results[0])

    API_success: bool = all(results)

    assert not API_success


def test_validate_inner_data_comment_not_string() -> None:
    """Test validate API when inner data has comment key whose value is not a string"""

    files = ["data/inner_data_comment_not_string.json"]
    results = []

    for file in files:
        # open a json file stored in data directory
        opening_results = device._open_json(file)

        # convert json object to json string
        inputData = json.dumps(opening_results[2])

        # call validate function and pass a json string
        validate_results = device.validate_JSON(inputData)

        # append validate_results to results list
        results.append(validate_results[0])

    API_success: bool = all(results)

    assert not API_success


def test_is_device_registered() -> None:
    """Test the function that checks if a device is registered."""

    devices_to_check = [9876, 1000, 1]
    expected_results = [True, True, False]

    check_results = []

    for dev in devices_to_check:
        result = device.is_device_registered(dev)
        check_results.append(result[0])

    assert check_results == expected_results


def test_register_devices_already_registered() -> None:
    """Test the function that registers devices."""

    devices_already_registered = [9876, 1000]
    expected_results = [False, False]

    check_results = []

    for dev in devices_already_registered:
        result = device.register_device(dev)
        check_results.append(result[0])

    assert check_results == expected_results


def test_remove_device_not_registered() -> None:
    """Test remove function with device not registered"""

    devices_to_remove = [1]

    expected_results = [False]

    check_results = []

    for dev in devices_to_remove:
        result = device.remove_device(dev)
        check_results.append(result[0])

    assert check_results == expected_results


def test_remove_device_registered() -> None:
    """Test remove function with device that is registered"""

    devices_to_remove = [123]

    expected_results = [True]

    check_results = []

    for dev in devices_to_remove:
        result = device.remove_device(dev)
        check_results.append(result[0])

    for dev in devices_to_remove:
        device.register_device(dev)

    assert check_results == expected_results


def test_registering_unregistered_device() -> None:
    """Test registering a device that is not currently registered"""

    devices_to_register = [1]

    expected_results = [True]

    check_results = []

    for dev in devices_to_register:
        result = device.register_device(dev)
        check_results.append(result[0])

    for dev in devices_to_register:
        device.remove_device(dev)

    assert check_results == expected_results
