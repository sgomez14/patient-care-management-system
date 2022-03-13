from typing import List
from datetime import datetime
import logging
import json
import os
import jsonschema
from jsonschema import validate
from chat_utils import *


valid_tokens = [4567]

chat_database = []


def validate_message_packet(chat_packet: str):
    """This function tests the submitted json against the chat json schema."""

    # first check if argument is a string
    if not isinstance(chat_packet, str):
        msg = "Validating Message Packet: The submitted packets is not a string."
        logging.error(msg)
        return [False, msg, ApiResult.CONFLICT.value]

    load_results = load_json_string(chat_packet)
    message_json = load_results[2]

    try:
        validate(instance=message_json, schema=chat_schema)
        msg = "Validating Message Packet: The submitted packets is valid."
        logging.info(msg)
        return [True, msg, ApiResult.SUCCESS.value]

    except jsonschema.exceptions.ValidationError as err:
        msg = "Validating Message Packet: The submitted packets is not valid."
        logging.error(msg)
        return [False, msg, ApiResult.CONFLICT.value, message_json]


def verify_chat_token(access_token: int):
    """This function checks if an access token is valid."""

    if not isinstance(access_token, int):
        msg = f"Verifying Access Token: Token \"{access_token}\" is not of type int."
        logging.error(msg)
        return [False, msg, ApiResult.CONFLICT.value]

    if access_token in valid_tokens:
        msg = f"Verifying Access Token: {access_token} is a valid token."
        logging.info(msg)
        return [True, msg, ApiResult.SUCCESS.value]
    else:
        msg = f"Verifying Access Token: {access_token} is not a valid token."
        logging.error(msg)
        return [False, msg, ApiResult.CONFLICT.value]


def store_chat_message(chat_packet: str):
    """This function stores the messages included in the chat message packet."""

    # first check if argument is a string
    if not isinstance(chat_packet, str):
        msg = "Store Chat Message: The packet past is not a string."
        logging.error(msg)
        return [False, msg, ApiResult.CONFLICT.value]

    # validate the chat message packet against schema
    validation_results = validate_message_packet(chat_packet)
    is_validation_successful = validation_results[0]

    if not is_validation_successful:
        return validation_results

    # extract the json from validation results, it is the last element in the results list
    message_json = validation_results[-1]

    # confirm that application sending chat packet has valid access token
    access_token = message_json["api_access_token"]

    access_results = verify_chat_token(access_token)
    is_token_valid = access_results[0]

    if not is_token_valid:
        return access_results

    # so far we have confirmed that the json matches the schema and the access token is valid
    # now we can write the chat message packet to the database
    writing_results = _write_to_chat_database(message_json)
    is_write_successful = writing_results[0]

    if is_write_successful:
        msg = "Store Chat Message: Successfully entered chat packet into database."
        logging.info(msg)
        return [True, msg, ApiResult.SUCCESS.value]
    else:
        msg = "Store Chat Message: Chat packet failed to write to database."
        logging.error(msg)
        return [True, msg, ApiResult.SUCCESS.value]


def _write_to_chat_database(chat_packet: dict):
    """This function writes the chat packet to the database."""

    # first check if argument is a dictionary
    if not isinstance(chat_packet, dict):
        msg = "Writing to Chat Database: The packet past is not correct data structure."
        logging.error(msg)
        return [False, msg, ApiResult.CONFLICT.value]

    chat_database.append(chat_packet)
    msg = "Writing to Chat Database: Successfully wrote chat packet to database."
    logging.info(msg)

    return [True, msg, ApiResult.SUCCESS.value]


if __name__ == '__main__':
    print("Hello, this is the chat module")

    test_json_examples = [chat_json_example, chat_json_wrong]

    for example in test_json_examples:

        message_packet = json.dumps(example)

        validate_result = validate_message_packet(message_packet)

        print(validate_result)
        print()
