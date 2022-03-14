# import json
import logging
import jsonschema
from jsonschema import validate
import pymongo
from pymongo import MongoClient
# from chat_utils import *
import chat_utils
from chat_utils import *

valid_tokens = [4567]


class ChatDB:
    cluster = MongoClient(f"mongodb+srv://{mongodb_user}:{mongodb_pwd}@pcms-database.xcbkd.mongodb.net/"
                          f"{mongodb_cluster}?retryWrites=true&w=majority")
    db = cluster["pcmsDB"]
    collection = db["chat"]

    @staticmethod
    def post_document(chat_packet: dict):
        """This function takes a chat_packet and insert the messages into the database."""

        # first check if argument is a dictionary
        if not isinstance(chat_packet, dict):
            msg = "Writing to Chat Database: The packet past is not correct data structure."
            logging.error(msg)
            return [False, msg, ApiResult.CONFLICT.value]

        message_owner = chat_packet["api_access_token"]
        documents = []

        for packet in chat_packet["message_packet"]:
            packet["message_owner"] = message_owner
            documents.append(packet)

        try:
            ChatDB.collection.insert_many(documents)
            msg = "Writing to Database: Operation successful."
            logging.info(msg)
            return [True, msg, ApiResult.SUCCESS.value]

        except pymongo.errors.PyMongoError as err:
            msg = "Writing to Database: Operation failed."
            logging.error(msg)
            return [False, msg, ApiResult.CONFLICT.value]

    @staticmethod
    def find_by_message_id(message_id: int):
        """This function finds a single message using the provided message_id"""

        # first check if argument is an int
        if not isinstance(message_id, int):
            msg = f"Querying Chat Database: message_id \"{message_id}\" is not type int."
            logging.error(msg)
            return [False, msg, ApiResult.CONFLICT.value]

        # define search filter
        find_filter = {"message_id": message_id}

        try:
            document = ChatDB.collection.find_one(filter=find_filter)

            if document is None:
                msg = f"Querying Chat Database: message_id \"{message_id}\" not found."
                logging.info(msg)
                return [False, msg, ApiResult.NOT_FOUND.value]
            else:
                msg = f"Querying Chat Database: Found message_id \"{message_id}\"."
                logging.info(msg)
                return [True, msg, ApiResult.SUCCESS.value, document]

        except pymongo.errors.PyMongoError as err:
            msg = f"Querying Chat Database: Checking for message_id \"{message_id}\" failed."
            logging.error(msg)
            return [False, msg, ApiResult.CONFLICT.value]

    @staticmethod
    def find_by_session_id(session_id: int):
        """This function finds all messages using the provided session_id"""

        # first check if argument is an int
        if not isinstance(session_id, int):
            msg = f"Querying Chat Database: session_id \"{session_id}\" is not type int."
            logging.error(msg)
            return [False, msg, ApiResult.CONFLICT.value]

        # define search filter
        find_filter = {"session_id": session_id}

        try:
            document_count = ChatDB.collection.count_documents(filter=find_filter)

            if document_count >= 1:
                documents = []
                query_results = ChatDB.collection.find(filter=find_filter)

                for doc in query_results:
                    documents.append(doc)

                msg = f"Querying Chat Database: Found messages for session_id \"{session_id}\"."
                logging.info(msg)
                return [True, msg, ApiResult.SUCCESS.value, documents]

            else:
                msg = f"Querying Chat Database: session_id \"{session_id}\" not found."
                logging.info(msg)
                return [False, msg, ApiResult.NOT_FOUND.value]

        except pymongo.errors.PyMongoError as err:
            msg = f"Querying Chat Database: Checking for session_id \"{session_id}\" failed."
            logging.error(msg)
            return [False, msg, ApiResult.CONFLICT.value]

    @staticmethod
    def find_by_message_owner(message_owner: int):
        """This function finds all messages using the provided message_owner"""

        # first check if argument is an int
        if not isinstance(message_owner, int):
            msg = f"Querying Chat Database: message_owner \"{message_owner}\" is not type int."
            logging.error(msg)
            return [False, msg, ApiResult.CONFLICT.value]

        # define search filter
        find_filter = {"message_owner": message_owner}

        try:
            document_count = ChatDB.collection.count_documents(filter=find_filter)

            if document_count >= 1:
                documents = []
                query_results = ChatDB.collection.find(filter=find_filter)

                for doc in query_results:
                    documents.append(doc)

                msg = f"Querying Chat Database: Found messages for message_owner \"{message_owner}\"."
                logging.info(msg)
                return [True, msg, ApiResult.SUCCESS.value, documents]

            else:
                msg = f"Querying Chat Database: message_owner \"{message_owner}\" not found."
                logging.info(msg)
                return [False, msg, ApiResult.NOT_FOUND.value]

        except pymongo.errors.PyMongoError as err:
            msg = f"Querying Chat Database: Checking for message_owner \"{message_owner}\" failed."
            logging.error(msg)
            return [False, msg, ApiResult.CONFLICT.value]


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
        return [True, msg, ApiResult.SUCCESS.value, message_json]

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

    # call to write to database
    write_results = ChatDB.post_document(chat_packet)
    write_successful = write_results[0]

    if write_successful:
        msg = "Writing to Chat Database: Successfully wrote chat packet to database."
        logging.info(msg)
        return [True, msg, ApiResult.SUCCESS.value]
    else:
        if write_successful:
            msg = "Writing to Chat Database: Writing chat packet to database failed."
            logging.error(msg)
            return [False, msg, ApiResult.CONFLICT.value]


if __name__ == '__main__':
    print("Hello, this is the chat module")

    # test_json_examples = [chat_json_example, chat_json_wrong]
    #
    # for example in test_json_examples:
    #
    #     message_packet = json.dumps(example)
    #
    #     validate_result = validate_message_packet(message_packet)
    #
    #     print(validate_result)
    #     print()
    #
    #     store_chat_message(message_packet)

    # post = {"_id": 1, "name": "santiago", "score": 5}
    # ChatDB.collection.delete_one(post)

    # print(ChatDB.find_by_message_id(1235))

    # results = ChatDB.find_by_session_id(9876)

    results = ChatDB.find_by_message_owner(4567)

    print(len(results[-1]))
    print(results[-1])

    for x in results[-1]:
        print(x)


