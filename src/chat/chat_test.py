# standard imports
import json

# local imports
from . import chat, chat_utils


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


