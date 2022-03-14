# standard imports
import json

# local imports
from . import chat, chat_utils
from .chat import ChatDB


def test_validate_message_packet() -> None:
    """This function tests the validate_message_packet.
    One valid json and one invalid json are passed.
    """

    test_json_examples = [chat_utils.chat_json_example, chat_utils.chat_json_wrong]

    test_results = []
    expected_results = [True, False]

    for example in test_json_examples:
        message_packet = json.dumps(example)

        validate_result = chat.validate_message_packet(message_packet)

        api_success = validate_result[0]

        test_results.append(api_success)

    assert test_results == expected_results


def test_validate_message_packet_wrong_input() -> None:
    """This function tests validate_message_packet with input that is not a string."""

    validate_results = chat.validate_message_packet(1234)
    test_results = validate_results[0]
    expect_results = False

    assert test_results == expect_results


def test_store_chat_message_wrong_input() -> None:
    """This function store_chat_message with input that is not a string."""

    store_results = chat.store_chat_message(1234)
    test_results = store_results[0]
    expect_results = False

    assert test_results == expect_results


def test_store_chat_message() -> None:
    """This function tests the store_chat_message.
    One valid json and one invalid json are passed.
    """

    test_json_examples = [chat_utils.chat_json_example, chat_utils.chat_json_wrong]

    test_results = []
    expected_results = [True, False]

    for example in test_json_examples:
        message_packet = json.dumps(example)

        validate_result = chat.validate_message_packet(message_packet)

        api_success = validate_result[0]

        test_results.append(api_success)

    assert test_results == expected_results


def test_verify_access_token() -> None:
    """This function tests verify_access_token."""

    test_token = [4567, 12, "890"]

    test_results = []
    expected_results = [True, False, False]

    for token in test_token:

        token_result = chat.verify_chat_token(token)

        api_success = token_result[0]

        test_results.append(api_success)

    assert test_results == expected_results


def test_find_by_message_id_not_found() -> None:
    """This function tests find_by_message_id when the message_id is not found."""

    message_id = 1236

    expected_result = [False, f'Querying Chat Database: message_id \"{message_id}\" not found.', 404]

    test_result = ChatDB.find_by_message_id(message_id)

    assert test_result == expected_result


def test_find_by_message_id_message_found() -> None:
    """This function tests find_by_message_id when the message_id is not found."""

    message_id = 1235

    document = json.dumps(chat_utils.mongo_chat_document1)

    expected_result = [True, f'Querying Chat Database: Found message_id \"{message_id}\".', 200, document]

    test_result = ChatDB.find_by_message_id(message_id)

    # remove the mongoDB generated document id
    test_result[-1].pop("_id")

    # standardize json
    return_document = json.dumps(test_result[-1])

    # put new standardize json in test_result
    test_result[-1] = return_document

    assert test_result == expected_result


def test_find_by_session_id_not_found() -> None:
    """This function tests find_by_session_id when the session_id is not found."""

    session_id = 1236

    expected_result = [False, f'Querying Chat Database: session_id \"{session_id}\" not found.', 404]

    test_result = ChatDB.find_by_session_id(session_id)

    assert test_result == expected_result


def test_find_by_session_id_message_found() -> None:
    """This function tests find_by_session_id when the session_id is found."""

    session_id = 9876

    expected_result = [True, f'Querying Chat Database: Found messages for session_id \"{session_id}\".', 200]

    test_result = ChatDB.find_by_session_id(session_id)

    # remove last element in result list
    test_result.pop(-1)

    assert test_result == expected_result


def test_find_by_message_owner_not_found() -> None:
    """This function tests find_by_message_owner when the message_owner is not found."""

    message_owner = 1236

    expected_result = [False, f'Querying Chat Database: message_owner \"{message_owner}\" not found.', 404]

    test_result = ChatDB.find_by_message_owner(message_owner)

    assert test_result == expected_result


def test_find_by_session_id_message_found() -> None:
    """This function tests find_by_message_owner when the message_owner is found."""

    message_owner = 4567

    expected_result = [True, f'Querying Chat Database: Found messages for message_owner \"{message_owner}\".', 200]

    test_result = ChatDB.find_by_message_owner(message_owner)

    # remove last element in result list
    test_result.pop(-1)

    assert test_result == expected_result


def test_sending_invalid_input_to_find_by_functions() -> None:
    """
    This function tests sending invalid inputs to the Chat database query methods.
    The query methods expect an int as input. But will provide different data type
    """

    # correct input would be an int
    invalid_input = "1234"

    expected_results = [False, False, False]

    test_results = [
        ChatDB.find_by_message_id(invalid_input)[0],
        ChatDB.find_by_session_id(invalid_input)[0],
        ChatDB.find_by_message_owner(invalid_input)[0]
    ]

    assert test_results == expected_results


