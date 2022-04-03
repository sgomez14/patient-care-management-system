import json
from src.users.users import UsersDB, authenticate_login


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
