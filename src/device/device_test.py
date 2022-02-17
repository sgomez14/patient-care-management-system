import device


def test_correct_temp_json() -> None:
    """Tests that JSON containing only temperature data has all correct keys"""

    input_file = "data/tempJSON.json"

    results = device.send_measurements(input_file)

    API_success: bool = results[0]

    assert API_success == True


def test_validate_temp_json() -> None:
    """Tests validate API call that JSON containing only temperature data has all correct keys and value types"""

    input_file = "data/tempJSON.json"

    results = device.validate_JSON(input_file)

    API_success: bool = results[0]

    assert API_success == True


def test_validate_temp_bp_json() -> None:
    """Tests validate API call that JSON containing temperature and blood pressure data has all correct keys"""

    input_file = "data/temp_bp.json"

    results = device.send_measurements(input_file)

    API_success: bool = results[0]

    assert API_success == True

