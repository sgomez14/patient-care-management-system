# standard imports
import json
import logging
import enum

# installed packages
import jsonschema
from jsonschema import validate


class DatabaseInfo:
    mongodb_pwd = "WgAVFP22prU8sVHW"
    mongodb_user = "sgomez22"
    mongodb_cluster = "PCMS-Database"


class ApiResult(enum.Enum):
    """This class enumerated codes to indicate the result of an API call."""

    SUCCESS = 200
    DEFAULT_FAIL = 400
    NOT_FOUND = 404
    CONFLICT = 409


def load_json_string(json_string: str):  # -> List[bool, str, ApiResult, json object]
    """This function loads dictionary from a json string"""

    # helper code from Kite.com
    # https://www.kite.com/python/answers/how-to-handle-json-decode-error-when-nothing-returns-in-python

    try:
        data = json.loads(json_string)
        msg = f"load_json_string: Successfully loaded JSON string called: {json_string}"
        logging.info(msg)
        return [True, msg, ApiResult.SUCCESS.value, data]

    except json.decoder.JSONDecodeError:
        data = {}
        msg = "load_json_string: String could not be converted to JSON"
        logging.error(msg)
        return [False, msg, ApiResult.SUCCESS.value, data]


def validate_json(json_string: str, json_schema: dict):
    """This function tests the submitted json against a given json schema."""

    # first check if argument is a string
    if not isinstance(json_string, str):
        msg = "Validating JSON: The submitted packet is not a string."
        logging.error(msg)
        return [False, msg, ApiResult.CONFLICT.value]

    # second check if argument is a dictionary
    if not isinstance(json_schema, dict):
        msg = "Validating JSON: The submitted schema is not a dictionary."
        logging.error(msg)
        return [False, msg, ApiResult.CONFLICT.value]

    load_results = load_json_string(json_string)

    if not load_results[0]:
        return load_results

    loaded_json = load_results[-1]

    try:
        validate(instance=loaded_json, schema=json_schema)
        msg = "Validating JSON: The submitted packet is valid."
        logging.info(msg)
        return [True, msg, ApiResult.SUCCESS.value, loaded_json]

    except jsonschema.exceptions.ValidationError as err:
        logging.error(f"Validating JSON: JSON schema exception -> {err}")
        msg = "Validating JSON: The submitted packet is not valid."
        logging.error(msg)
        return [False, msg, ApiResult.CONFLICT.value, loaded_json]