import json
from src.users.users import UsersDB, authenticate_login, get_user_assignments


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
