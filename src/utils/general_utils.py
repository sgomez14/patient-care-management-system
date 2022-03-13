import json
import logging
import enum


class ApiResult(enum.Enum):
    """This class enumerated codes to indicate the result of an API call."""

    SUCCESS = 200
    DEFAULT_FAIL = 400
    NOT_FOUND = 404
    CONFLICT = 409


def load_json_string(json_string: str):  # -> List[bool, str, ApiResult, json object]
    """This function loads json from a string"""

    # helper code from Kite.com
    # https://www.kite.com/python/answers/how-to-handle-json-decode-error-when-nothing-returns-in-python

    try:
        data = json.loads(json_string)
        msg = f"_load_json_string: Successfully loaded JSON string called: {json_string}"
        logging.info(msg)
        return [True, msg, data, ApiResult.SUCCESS.value]

    except json.decoder.JSONDecodeError:
        data = {}
        msg = "_load_json_string: String could not be converted to JSON"
        logging.error(msg)
        return [False, msg, data, ApiResult.CONFLICT.value]