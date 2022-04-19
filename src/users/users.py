import json
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


class AssignmentsDB:
    cluster = MongoClient(f"mongodb+srv://{dbInfo.mongodb_user}:{dbInfo.mongodb_pwd}@pcms-database.xcbkd.mongodb.net/"
                          f"{dbInfo.mongodb_cluster}?retryWrites=true&w=majority")
    db = cluster["pcmsDB"]
    collection = db["assignments"]

    @staticmethod
    def getAssignments(user_id: int):
        """This function finds all of the assignments for user_id."""

        DOCTOR = "doctor"
        PATIENT = "patient"

        # first check if argument is an int
        if not isinstance(user_id, int):
            msg = f"Querying Assignments Database: user_id \"{user_id}\" is not type int."
            logging.error(msg)
            return [False, msg, ApiResult.CONFLICT.value]

        # define search filter
        find_filter = {"$or": [{"doctor.user_id": user_id}, {"patient.user_id": user_id}]}

        try:
            # query database
            assignments = AssignmentsDB.collection.find(filter=find_filter)

            if assignments.retrieved != 0:
                msg = f"Querying Assignments Database: No assignments found for user_id \"{user_id}\"."
                logging.info(msg)
                return [False, msg, ApiResult.NOT_FOUND.value]

            else:
                msg = f"Querying Assignments Database: Found assignments for user_id \"{user_id}\"."
                logging.info(msg)

                assign_data = []

                for assignment in assignments:

                    # create template data dictionary that temporary stores info for a single assignment
                    data = {"user_id": 0, "name": ""}

                    # remove the mongoDB _id key so that document can be serialized into JSON string
                    assignment.pop("_id")

                    # grab the doctor and patient ids
                    doctor_id = assignment["doctor"]["user_id"]
                    patient_id = assignment["patient"]["user_id"]

                    # grab user's first and last names
                    if user_id != doctor_id:  # this means user_id belongs to patient, so we need to grab doctor records

                        # query user database to get first and last names
                        full_name_results = UsersDB.get_user_fullname(doctor_id)

                        # check if finding the user was successful
                        if full_name_results[0]:
                            full_name = full_name_results[-1] # data is returned in the last index
                            data["user_id"] = doctor_id
                            data["name"] = full_name

                            # append assignment record to the dictionary tracking all of the assignments
                            assign_data.append(data)

                        else:  # the find user query failed
                            return full_name_results

                    elif user_id != patient_id:  # this means user_id belongs to doctor, must grab patient records

                        # query user database to get first and last names
                        full_name_results = UsersDB.get_user_fullname(patient_id)

                        # check if finding the user was successful
                        if full_name_results[0]:
                            full_name = full_name_results[-1]  # data is returned in the last index
                            data["user_id"] = patient_id
                            data["name"] = full_name

                            # append assignment record to the dictionary tracking all of the assignments
                            assign_data.append(data)

                    else:  # there user_id found in the assignments database is not in the users database
                        msg = f"Querying Assignments Database: Mismatch in database for user_id \"{user_id}\"."
                        logging.error(msg)
                        return [False, msg, ApiResult.CONFLICT.value]

                # convert dictionary into JSON string
                # assign_data = json.dumps(assign_data)

                return [True, msg, ApiResult.SUCCESS.value, assign_data]

        except pymongo.errors.PyMongoError as err:
            logging.error(f"Debugging Users Database: mongo exception -> {err}")
            msg = f"Querying Users Database: Checking for user_id \"{user_id}\" failed."
            logging.error(msg)
            return [False, msg, ApiResult.CONFLICT.value]


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

    @staticmethod
    def get_user_fullname(user_id: int):
        """This function gets full name associated with user_id"""

        # first check if argument is an int
        if not isinstance(user_id, int):
            msg = f"Querying Users Database: user_id \"{user_id}\" is not type int."
            logging.error(msg)
            return [False, msg, ApiResult.CONFLICT.value]

        # query user database to get first and last names
        find_user_results = UsersDB.find_user(user_id)

        # check if finding the user was successful
        if find_user_results[0]:
            first_name = find_user_results[-1]["first_name"]  # data is returned in the last index
            last_name = find_user_results[-1]["last_name"]    # data is returned in the last index

            # concatenate first and last name
            full_name = f"{first_name} {last_name}"

            # log result
            msg = f"Querying User Database: Full name for user_id \"{user_id}\" is {full_name}"
            logging.info(msg)

            return [True, msg, ApiResult.SUCCESS.value, full_name]

        else:  # the find user query failed
            return find_user_results


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
    roles = user_record["roles"]

    if passwords_match:
        msg = "Authenticating Login: Authentication successful."
        logging.info(msg)
        return [True, msg, ApiResult.SUCCESS.value, roles]
    else:
        msg = "Authenticating Login: Authentication not successful."
        logging.info(msg)
        return [False, msg, ApiResult.CONFLICT.value, "n/a"]


def get_user_assignments(user_id):

    return AssignmentsDB.getAssignments(user_id)





