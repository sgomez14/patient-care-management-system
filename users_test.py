import json
from src.users.users import UsersDB, authenticate_login, get_user_assignments, get_patient_summary,\
    get_most_recent_measurement, get_all_recent_measurements


def test_find_user_in_db() -> None:
    """This function tests finding a user that exists in the database."""
    user_id = 42530
    find_result = UsersDB.find_user(user_id)

    test_result = find_result[0]

    expected_result = True

    assert test_result == expected_result


def test_find_user_not_in_db() -> None:
    """This function tests finding a user that does not exist in the database."""
    user_id = 42
    find_result = UsersDB.find_user(user_id)

    test_result = find_result[0]

    expected_result = False

    assert test_result == expected_result


def test_authenticate_login_valid() -> None:
    """This function tests authenticating a user login that is valid."""

    login_json = '{"user_id": 42530, "password": "ec530"}'

    # login_json = json.dumps(login_json)

    authenticate_login_results = authenticate_login(login_json)

    test_result = authenticate_login_results[0]

    expected_result = True

    assert test_result == expected_result


def test_authenticate_login_not_valid_wrong_password() -> None:
    """This function tests authenticating a user login that is not valid."""

    login_json = {'user_id': 42530, 'password': 'helloworld'}

    login_json = json.dumps(login_json)

    authenticate_login_results = authenticate_login(login_json)

    test_result = authenticate_login_results[0]

    expected_result = False

    assert test_result == expected_result


def test_get_assignments_with_valid_user_id() -> None:
    """This function tests getting the assignments for user_ids."""

    test_cases = [123, 321]

    expected_result = [
        [True, 'Querying Assignments Database: Found assignments for user_id "123".', 200,
         [{'user_id': 321, 'name': 'test_patient_first test_patient_last'}]],
        [True, 'Querying Assignments Database: Found assignments for user_id "321".', 200,
         [{'user_id': 123, 'name': 'test_doctor_first test_doctor_last'}]]

    ]

    test_result = []

    for test_case in test_cases:
        result = get_user_assignments(test_case)

        test_result.append(result)

    assert test_result == expected_result


def test_get_assignments_with_invalid_user_id() -> None:
    """This function tests getting the assignments for invalid user_ids."""

    test_cases = [12]

    expected_result = [
        [False, 'Querying Users Database: user_id "12" not found.', 404]

    ]

    test_result = []

    for test_case in test_cases:
        result = get_user_assignments(test_case)

        test_result.append(result)

    assert test_result == expected_result


def test_get_patient_summary_with_valid_user_id() -> None:
    """This function tests getting the patient summaries for user_ids."""

    test_cases = [321, 123]

    expected_result = [
        [True, 'Querying User Database: Full name for user_id "321" is test_patient_first test_patient_last', 200,
         {'user_id': 321, 'name': 'test_patient_first test_patient_last', 'height': '5 ft. 1 in.', 'weight': '150 lbs.',
          'allergies': ['rain'], 'medication': ['happiness'], 'medical_conditions': ['high blood pressure']}],

        [False, 'Querying Users Database: user_id "123" does not have a summary entry in their record.', 404]
    ]

    test_result = []

    for test_case in test_cases:
        result = get_patient_summary(test_case)

        test_result.append(result)

    assert test_result == expected_result


def test_get_patient_summary_with_invalid_user_id() -> None:
    """This function tests getting the patient summaries with invalid user_ids."""

    test_cases = [12]

    expected_result = [
        [False, 'Querying Users Database: user_id "12" not found.', 404]
    ]

    test_result = []

    for test_case in test_cases:
        result = get_patient_summary(test_case)

        test_result.append(result)

    assert test_result == expected_result


def test_get_most_recent_measurement() -> None:
    """Test getting the most recent measurement of a given type for a user.
    The test includes accessing measurements the patient has and does not have."""

    test_user_id = 321
    test_cases = ["temperature", "BP"]

    expected_result = [
        [True, 'Querying Measurements Database: Found most recent "temperature" measurement for user_id "321".', 200,
         '100.1 F Date: 2022-04-27 00:35:28'],
        [False, 'Querying Measurements Database: no "BP" measurement for user_id "321".', 404]
    ]

    test_result = []
    for test_case in test_cases:
        result = get_most_recent_measurement(test_user_id, test_case)

        test_result.append(result)

    assert test_result == expected_result


def test_get_all_recent_measurement() -> None:
    """Test getting all recent measurements for a user."""

    test_cases = [321]

    expected_result = [
        [True, 'Querying Measurements Database: Getting all recent measurement for user_id "321" succeeded.', 200,
         {'temperature': '100.1 F Date: 2022-04-27 00:35:28',
          'blood_pressure': '115/70 mmHg Date: 2022-04-27 00:45:28',
          'pulse': 'Measurement not in record.',
          'oximeter': 'Measurement not in record.',
          'weight': 'Measurement not in record.',
          'glucometer': 'Measurement not in record.'}
         ]
    ]

    test_result = []
    for test_case in test_cases:
        result = get_all_recent_measurements(test_case)

        test_result.append(result)

    assert test_result == expected_result
