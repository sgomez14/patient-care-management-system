import logging
import pymongo
from pymongo import MongoClient

from ..utils.general_utils import ApiResult, load_json_string, DatabaseInfo as dbInfo, validate_json
# from users_utils.users_utils import login_schema

login_schema = {
    "$schema": "http://json-schema.org/draft-06/schema#",
    "$ref": "#/definitions/Login",
    "definitions": {
        "Login": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "user_id": {
                    "type": "integer"
                },
                "password": {
                    "type": "string"
                }
            },
            "required": [
                "password",
                "user_id"
            ],
            "title": "Login"
        }
    }
}


class UserRoles:
    OTHER: int = -1
    PATIENT: int = 0
    DOCTOR: int = 1
    NURSE: int = 2
    ADMIN: int = 3


class UsersDB:
    cluster = MongoClient(f"mongodb+srv://{dbInfo.mongodb_user}:{dbInfo.mongodb_pwd}@pcms-database.xcbkd.mongodb.net/"
                          f"{dbInfo.mongodb_cluster}?retryWrites=true&w=majority")
    db = cluster["pcmsDB"]
    collection = db["users"]

    @staticmethod
    def find_user(user_id: int):
        """This function finds a user with user_id"""

        # first check if argument is an int
        if not isinstance(user_id, int):
            msg = f"Querying Users Database: user_id \"{user_id}\" is not type int."
            logging.error(msg)
            return [False, msg, ApiResult.CONFLICT.value]

        # define search filter
        find_filter = {"user_id": user_id}

        try:
            # query database
            document = UsersDB.collection.find_one(filter=find_filter)

            if document is None:
                msg = f"Querying Users Database: user_id \"{user_id}\" not found."
                logging.info(msg)
                return [False, msg, ApiResult.NOT_FOUND.value]

            else:
                msg = f"Querying Users Database: Found user_id \"{user_id}\"."
                logging.info(msg)

                # remove the mongoDB _id key so that document can be serialized into JSON string
                document.pop("_id")

                return [True, msg, ApiResult.SUCCESS.value, document]

        except pymongo.errors.PyMongoError as err:
            logging.error(f"Debugging Users Database: mongo exception -> {err}")
            msg = f"Querying Users Database: Checking for user_id \"{user_id}\" failed."
            logging.error(msg)
            return [False, msg, ApiResult.CONFLICT.value]

    # @staticmethod
    # def post_document(chat_packet: dict):
    #     """This function takes a chat_packet and insert the messages into the database."""
    #
    #     # first check if argument is a dictionary
    #     if not isinstance(chat_packet, dict):
    #         msg = "Writing to Chat Database: The packet past is not correct data structure."
    #         logging.error(msg)
    #         return [False, msg, ApiResult.CONFLICT.value]
    #
    #     message_owner = chat_packet["api_access_token"]
    #     documents = []
    #
    #     for packet in chat_packet["message_packet"]:
    #         packet["message_owner"] = message_owner
    #         documents.append(packet)
    #
    #     try:
    #         ChatDB.collection.insert_many(documents)
    #         msg = "Writing to Database: Operation successful."
    #         logging.info(msg)
    #         return [True, msg, ApiResult.SUCCESS.value]
    #
    #     except pymongo.errors.PyMongoError as err:
    #         msg = "Writing to Database: Operation failed."
    #         logging.error(msg)
    #         return [False, msg, ApiResult.CONFLICT.value]


def authenticate_login(login_json: str):

    # first check if argument is a string
    if not isinstance(login_json, str):
        msg = f"Querying Users Database: login parameter is not type string."
        logging.error(msg)
        return [False, msg, ApiResult.CONFLICT.value]

    validate_json_results = validate_json(login_json, login_schema)

    # check if the json validation is successful
    if not validate_json_results[0]:
        return validate_json_results

    # the loaded json string is in the last element
    login_credentials = validate_json_results[-1]

    # since the login json validated against its schema, its contents can now me extracted
    user_id = login_credentials["user_id"]
    password = login_credentials["password"]

    # check database for user
    find_user_results = UsersDB.find_user(user_id)

    if not find_user_results[0]:
        return find_user_results

    # grab the user record from the database query
    user_record = find_user_results[-1]

    # validate password
    passwords_match = password == user_record["password"]

    if passwords_match:
        msg = "Authenticating Login: Authentication successful."
        logging.info(msg)
        return [True, msg, ApiResult.SUCCESS.value]
    else:
        msg = "Authenticating Login: Authentication not successful."
        logging.info(msg)
        return [False, msg, ApiResult.CONFLICT.value]





