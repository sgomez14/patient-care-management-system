from typing import List
from datetime import datetime
import logging
import json
import os
import enum

# this is the temporary database for the devices
registered_devices: dict = {"device_ids": [9876, 1000, 123]}

# temp database for storing
local_database = {}


# Using enums
# https://www.geeksforgeeks.org/enum-in-python/
class EditDevice(enum.Enum):
    """This class enumerated codes for various edit device operations."""

    REGISTER = 0
    UPDATE = 1
    REMOVE = 2


class ApiResult(enum.Enum):
    """This class enumerated codes to indicate the result of an API call."""

    SUCCESS = 200
    DEFAULT_FAIL = 400
    NOT_FOUND = 404
    CONFLICT = 409


def send_measurements(json_file: str, passing_a_file=False):  # -> List[bool, str]:
    """This function receives a JSON file and returns a list.
       The list index 0 indicates success of function and index 1 provides a status message"""

    # validate JSON file
    validate_JSON_format_results = validate_JSON(json_file, passing_a_file=passing_a_file)

    if not validate_JSON_format_results[0]:
        return validate_JSON_format_results

    # write json data to database
    json_data = validate_JSON_format_results[3]
    database_write_result = _write_to_database(json_data)

    return database_write_result


def _is_JSON_file(file: str):  # -> List[bool, str, ApiResult]:
    """Returns file type as string else it returns invalidFileName"""

    logging.info("Determining file type.")

    # checking if the argument passed is a string
    if isinstance(file, str):

        # tokenize the file string into file name and type
        fileName = file.split(".")

        # split returns list with only one element if delimiter not present in string
        if len(fileName) > 1:

            logging.info(f"User passed \"{file}\" as file name.")

            # extract the file type
            fileType = fileName[1]

            logging.info(f"The file extension is: {fileType}")

            result: bool = fileType.lower() == "json"

            msg = ""
            if result:
                msg = f"{file} file has the JSON extension"
                logging.info(msg)
            else:
                msg = f"invalidFileName: \"{file}\" is not a valid file name"
                logging.error(msg)

            return [result, msg, ApiResult.SUCCESS.value]

        else:
            msg = f"invalidFileName: \"{file}\" is not a valid file name"
            logging.error(msg)
            return [False, msg, ApiResult.CONFLICT.value]
    else:
        return [False, f"Value \"{file}\" is not of type string.", ApiResult.CONFLICT.value]


def validate_JSON(json_file: str, passing_a_file=False):  # -> List[bool, str, ApiResult, dict]:
    """This function checks that the json adheres to the device module's json schema"""

    # this variable will contain the JSON data
    data = {}

    # check if json_file argument is a file instead of a JSON string
    if passing_a_file:
        is_JSON_file_results: List[bool, str] = _is_JSON_file(json_file)

        # check that the file is a json
        if not is_JSON_file_results[0]:
            warning: str = "User did not pass a json file"
            logging.error(warning)
            return [False, warning, ApiResult.CONFLICT.value]

        # open the json file
        open_json_results = _open_json(json_file)

        if not open_json_results[0]:
            return open_json_results

        # at this stage json file opened properly, need to extract json data from opening results
        data = open_json_results[2]
    else:

        # load the json string
        load_json_string_results = _load_json_string(json_file)
        if not load_json_string_results[0]:
            msg = f"{load_json_string_results[1]}"
            load_json_string_results[1] = msg
            logging.error(msg)
            return load_json_string_results

        # at this stage json string loaded properly, need to extract json data from loading results
        data = load_json_string_results[2]

    # check primaryKeys
    primaryKeys = list(data.keys())
    primaryKeys_check_results = _check_primary_keys(primaryKeys, data)

    if not primaryKeys_check_results[0]:
        return primaryKeys_check_results

    # check if device is registered
    check_device_registered_result = is_device_registered(data["deviceID"])

    if not check_device_registered_result[0]:
        return check_device_registered_result

    # check measurementKeys
    measureKeys = list(data["measurements"].keys())
    measureKeys_check_results = _check_measurement_keys(measureKeys, data)

    if not measureKeys_check_results[0]:
        return measureKeys_check_results

    # check metadataKeys
    for key in measureKeys:
        # pass the list of dictionaries
        inner_data_list = data["measurements"][key]

        # check metadata keys within the inner data packet
        metadata_check_results = _check_metadata_keys(key, inner_data_list)

        if not metadata_check_results[0]:
            return metadata_check_results

    # opening JSON file successful
    openResult = "JSON format is correct"

    return [True, openResult, ApiResult.SUCCESS.value, data]


def _check_primary_keys(keys: List[str], json_data: json):  # -> List[bool, str, ApiResult]:
    primary_keys: List[str] = ["patientID", "deviceID", "deviceType", "measurements"]

    # check that json has four primary keys
    if len(keys) != len(primary_keys):
        msg = "Missing primary keys"
        logging.error(msg)
        return [False, msg, ApiResult.CONFLICT.value]

    # check that key only appears once
    for key in keys:
        key_occurrence = primary_keys.count(key)
        if key_occurrence != 1:
            msg = f"incorrect key in data structure: \"{key}\" or it appears multiple times"
            logging.error(msg)
            return [False, msg, ApiResult.CONFLICT.value]

    # at this point we have confirmed that each key from user file matches primary keys in schema
    # now we can use the primary keys to check the data types for each key/value pair
    # patientID: int, deviceID = int, deviceType: int, measurements: dict
    for key in primary_keys:
        if key == "measurements":
            if not isinstance(json_data[key], dict):
                msg = f"measurements key does not have a dictionary assigned to it. Value provided: {json_data[key]}"
                logging.error(msg)
                return [False, msg, ApiResult.CONFLICT.value]

            if len(json_data[key]) == 0:
                msg = f"measurements key's dictionary is empty. Value provided: {json_data[key]}"
                logging.error(msg)
                return [False, msg, ApiResult.CONFLICT.value]
        else:
            if not isinstance(json_data[key], int):
                msg = f"{key} key does not have an int value assigned to it. Value provided: {json_data[key]}"
                logging.error(msg)
                return [False, msg, ApiResult.CONFLICT.value]

    # the primary keys and their respective value validate
    return [True, "all keys correct with corresponding value type", ApiResult.SUCCESS.value]


def _check_measurement_keys(keys: List[str], json_data: json):  # -> List[bool, str, ApiResult]:
    """This function verifies the keys and values in measurements data structure"""

    # measure_key is the string for the name of the measurements key
    measure_key = "measurements"
    measurement_keys = ["temperature", "blood_pressure", "pulse", "oximeter",
                        "weight", "glucometer"]

    # check that key only appears once
    for key in keys:
        key_occurrence = measurement_keys.count(key)
        if key_occurrence != 1:
            msg = f"incorrect key in data structure: measurement key \"{key}\"  or it appears multiple times"
            logging.error(msg)
            return [False, msg, ApiResult.CONFLICT.value]

        # first index into measurements dictionary and then index by each key within the measurements dictionary
        # each measurement key needs to have a list
        if not isinstance(json_data[measure_key][key], list):
            msg = f"{key} key does not have a list value assigned to it. Value provided: {json_data[measure_key][key]}"
            logging.error(msg)
            return [False, msg, ApiResult.CONFLICT.value]

        # check that list is not empty
        if len(json_data[measure_key][key]) == 0:
            msg = f"{key} key has an empty list assigned to it. Value provided: {json_data[measure_key][key]}"
            logging.error(msg)
            return [False, msg, ApiResult.CONFLICT.value]

    # the measurement keys and their respective value validate
    return [True, "all measurement keys are valid and have an accompanying list", ApiResult.SUCCESS.value]


def _check_metadata_keys(measurement_key: str, data: List[dict]):  # -> List[bool, str, ApiResult]:
    metadata_keys: List[str] = ["unit", "timestamp", "comments"]

    # each measurement_key will have a list that can contain
    # multiple inner dictionaries encapsulating the device's measurement data
    for data_dict in data:
        # grab the keys within the dictionary
        metaKeys = list(data_dict.keys())

        # check that inner data packet has correct number of keys
        expected_num_keys = 1+len(metadata_keys)
        if len(metaKeys) != expected_num_keys:
            msg = f"Incorrect number of inner data keys. Expected {expected_num_keys} keys," \
                  f" but received {len(metaKeys)} keys."
            logging.error(msg)
            return [False, msg, ApiResult.CONFLICT.value]

        # measurement_key must be present in inner data packet
        measurement_key_occurrence = metaKeys.count(measurement_key)
        if measurement_key_occurrence != 1:
            msg = f"{measurement_key} measurement key is not in inner data packet."
            logging.error(msg)
            return [False, msg, ApiResult.CONFLICT.value]

        # remove measurement_key temporarily to check metadata_keys are correct
        metaKeys.remove(measurement_key)
        for key in metaKeys:
            key_occurrence = metadata_keys.count(key)
            if key_occurrence != 1:
                logging.error("error is happening in check_metadata_keys")
                msg = f"key: {key}, key_occurrence: {key_occurrence}, it must once, or this key is not supported." \
                      f"supported metadata_keys are: {metadata_keys}"
                logging.error(msg)
                return [False, msg, ApiResult.CONFLICT.value]

        # reinsert measurement key into list
        metaKeys.append(measurement_key)

        # check that keys for blood_pressure dictionary are named systolic and diastolic
        if measurement_key == "blood_pressure":
            # blood pressure dictionary must have two keys: systolic and diastolic
            elements_in_blood_pressure_dict: int = 2

            if len(data_dict[measurement_key]) != elements_in_blood_pressure_dict:
                msg = f"there are not enough keys in the {measurement_key} dictionary"
                logging.error(msg)
                return [False, msg, ApiResult.CONFLICT.value]

            for key in data_dict[measurement_key].keys():
                # check that keys are either systolic or diastolic
                if key != "systolic" and key != "diastolic":
                    msg = f"{key} key in the {measurement_key} dictionary is not named systolic or diastolic"
                    logging.error(msg)
                    return [False, msg, ApiResult.CONFLICT.value]

        # verify the measurement values attached to the inner data packet measurement key
        measurement = data_dict[measurement_key]
        unit = data_dict["unit"]
        verify_measurement_range_results = _verify_measurement_range(measurement_key, measurement, unit)
        if not verify_measurement_range_results[0]:
            return verify_measurement_range_results

        # confirmed that measurement_key is in inner data packet, now can safely remove & continue checking other keys
        metaKeys.remove(measurement_key)

        # validate metadata keys values
        for key in metaKeys:
            # checking timestamp value
            if key == "timestamp":
                verify_timestamp_result = _verify_timestamp(data_dict[key])

                if not verify_timestamp_result[0]:
                    return verify_timestamp_result

            # checking unit value
            elif key == "unit":
                verify_units_result = _verify_units(measurement_key, data_dict[key])

                if not verify_units_result[0]:
                    return verify_units_result

            else:
                # checking that the comments are actually a string
                if not isinstance(data_dict[key], str):
                    msg = f"{key} key has value {data_dict[key]} but it must be a string"
                    logging.error(msg)
                    return [False, msg, ApiResult.CONFLICT.value]

    msg = "Inner data keys and values validated"
    logging.info(msg)
    return [True, msg, ApiResult.SUCCESS.value]


def _write_to_database_file(json_data: dict):  # -> List[bool, str, ApiResult]:
    database: str = "data/database.json"
    try:
        with open(database, "w") as json_file:
            json.dump(json_data, json_file, indent=4)

        message = "JSON data successfully written to database"
        logging.info(message)
        return [True, message, ApiResult.SUCCESS.value]

    except IOError:
        message = "Could not write json data to database"
        logging.error(message)

        return [False, message, ApiResult.DEFAULT_FAIL.value]


def _write_to_database(json_data: dict):  # -> List[bool, str, ApiResult]:

    if not isinstance(json_data, dict):
        msg = "Write to database: arguments passed were not dictionaries"
        logging.error(msg)
        return [False, msg, ApiResult.CONFLICT.value]

    local_database = json_data
    msg = "Write to database: Successfully added device measurements to database."
    logging.info(msg)

    return [True, msg, ApiResult.SUCCESS.value]




def _verify_units(measurement_key: str, unit: str):  # -> List[bool, str, ApiResult]
    supported_measurements = ["temperature", "blood_pressure", "pulse", "oximeter",
                              "weight", "glucometer"]

    supported_units = {"temperature": ["F", "C"], "blood_pressure": "mmHg", "pulse": "bpm", "oximeter": "%",
                       "weight": ["lbs", "kg"], "glucometer": "mg/dl"}

    result: bool = False

    if measurement_key not in supported_measurements:
        msg = f"{measurement_key} is not a supported measurement key"
        logging.error(msg)
        return [False, msg, ApiResult.CONFLICT.value]

    if measurement_key == "temperature":
        if unit.upper() == supported_units[measurement_key][0] or unit.upper() == supported_units[measurement_key][1]:
            result = True
        else:
            result = False

    elif measurement_key == "blood_pressure":
        if unit == supported_units[measurement_key]:
            result = True
        else:
            result = False

    elif measurement_key == "pulse":
        if unit.lower() == supported_units[measurement_key]:
            result = True
        else:
            result = False

    elif measurement_key == "oximeter":
        if unit == supported_units[measurement_key]:
            result = True
        else:
            result = False

    elif measurement_key == "weight":
        if unit.lower() == supported_units[measurement_key][0] or unit.lower() == supported_units[measurement_key][1]:
            result = True
        else:
            result = False

    elif measurement_key == "glucometer":
        if unit == supported_units[measurement_key]:
            result = True
        else:
            result = False

    if result:
        msg = f"{unit} unit for {measurement_key} validated"
        logging.info(msg)
        return [True, msg, ApiResult.SUCCESS.value]
    else:
        msg = f"{unit} unit is not valid unit for {measurement_key}."
        logging.error(msg)
        return [False, msg, ApiResult.CONFLICT.value]


def _verify_timestamp(timestamp: str):  # -> List[bool, str, ApiResult]
    """This function verifies that timestamp adheres to ISO 8601 standard"""

    iso8601_format: str = "%Y-%m-%dT%H:%M:%S"

    if not isinstance(timestamp, str):
        msg = f"{timestamp} timestamp must be a string"
        logging.error(msg)
        return [False, msg, ApiResult.CONFLICT.value]

    try:
        if datetime.strptime(timestamp, iso8601_format):
            msg = f"{timestamp} timestamp validated."
            logging.info(msg)
            return [True, msg, ApiResult.SUCCESS.value]

        else:
            msg = f"provided timestamp {timestamp} does not adhere to ISO8601 standard," \
                  f" eg. 1991-10-28T01:30:58"
            logging.error(msg)
            return [False, msg, ApiResult.CONFLICT.value]
    except ValueError:
        msg = f"provided timestamp {timestamp} does not adhere to ISO8601 standard," \
              f" eg. 1991-10-28T01:30:58"
        logging.error(msg)
        return [False, msg, ApiResult.CONFLICT.value]


def _verify_measurement_range(measurement_type: str, measurement, unit: str):  # -> List[bool, str, ApiResult]
    # lowest temp: https://www.guinnessworldrecords.com/world-records/67747-lowest-body-temperature
    # highest temp: https://www.npr.org/sections/goatsandsoda/2014/11/14/364060441/you-might-be-surprised-when-you-take-your-temperature

    # max blood pressure: https://pubmed.ncbi.nlm.nih.gov/7741618/#:~:text=The%20highest%20pressure%20recorded%20in,005)

    # lowest pulse: https://www.guinnessworldrecords.com/world-records/lowest-heart-rate
    # highest pulse: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3273956/

    # highest weight: https://www.guinnessworldrecords.com/news/2018/12/history-of-heaviest-humans-as-worlds-biggest-man-loses-half-his-body-weight-550495

    # highest glucose: https://www.guinnessworldrecords.com/world-records/highest-blood-sugar-level

    supported = {"temperature": {"min": {"F": 53, "C": 11}, "max": {"F": 115, "C": 46}},
                 "blood_pressure": {"min": {"systolic": 0, "diastolic": 0}, "max": {"systolic": 370, "diastolic": 360}},
                 "pulse": {"min": 27, "max": 480},
                 "oximeter": {"min": 0, "max": 100},
                 "weight": {"min": {"lbs": 0, "kg": 0}, "max": {"lbs": 946, "kg": 429}},
                 "glucometer": {"min": 0, "max": 2656}}

    # check that measurement_type value is a string
    if not isinstance(measurement_type, str):
        msg = f"Passed {measurement_type} as a measurement_type, but expected a string."
        logging.error(msg)
        return [False, msg, ApiResult.CONFLICT.value]

    # check the measurement_type is supported, the count must equal 1 to indicate that measurement_type is supported
    if list(supported.keys()).count(measurement_type) != 1:
        msg = f"Passed {measurement_type} as a measurement_type, but it is not supported." \
              f"Supported measurement types are {list(supported.keys())}"
        logging.error(msg)
        return [False, msg, ApiResult.CONFLICT.value]

    # check that the units are correct
    verify_units_result = _verify_units(measurement_type, unit)
    if not verify_units_result[0]:
        return verify_units_result

    # check that measurement value is int or float
    # blood_pressure measurement needs special processing since it is passed a dictionary with two inner measurements
    measurement_list = []
    if measurement_type == "blood_pressure":
        measurement_list.append(measurement["systolic"])
        measurement_list.append(measurement["diastolic"])
    else:
        measurement_list.append(measurement)

    for reading in measurement_list:
        if not isinstance(reading, (int, float)):
            msg = f"Passed {reading} as a measurement, but expected an int or float."
            logging.error(msg)
            return [False, msg, ApiResult.CONFLICT.value]

    MIN = 0
    MAX = 100

    # grab max and min from dictionary
    if measurement_type == "temperature":
        MAX = supported[measurement_type]["max"][unit]
        MIN = supported[measurement_type]["min"][unit]

    elif measurement_type == "weight":
        MAX = supported[measurement_type]["max"][unit]
        MIN = supported[measurement_type]["min"][unit]

    elif measurement_type == "blood_pressure":
        MAX_SYSTOLIC = supported[measurement_type]["max"]["systolic"]
        MIN_SYSTOLIC = supported[measurement_type]["min"]["systolic"]

        MAX_DIASTOLIC = supported[measurement_type]["max"]["diastolic"]
        MIN_DIASTOLIC = supported[measurement_type]["min"]["diastolic"]

        systolic_reading = measurement["systolic"]
        diastolic_reading = measurement["diastolic"]

    else:
        MAX = supported[measurement_type]["max"]
        MIN = supported[measurement_type]["min"]

    # check that measurements are within expected ranges
    if measurement_type == "blood_pressure":
        min_bp = "min"
        max_bp = "max"
        if systolic_reading < MIN_SYSTOLIC or systolic_reading > MAX_SYSTOLIC:
            msg = f"{measurement_type} measurement of {measurement} is not in valid range." \
                  f" MIN: {supported[measurement_type][min_bp]}, MAX: {supported[measurement_type][max_bp]}."
            logging.error(msg)
            return [False, msg, ApiResult.CONFLICT.value]

        if diastolic_reading < MIN_DIASTOLIC or diastolic_reading > MAX_DIASTOLIC:
            msg = f"{measurement_type} measurement of {measurement} is not in valid range." \
                  f" MIN: {supported[measurement_type][min_bp]}, MAX: {supported[measurement_type][max_bp]}."
            logging.error(msg)
            return [False, msg, ApiResult.CONFLICT.value]

    else:
        if measurement < MIN or measurement > MAX:
            msg = f"{measurement_type} measurement of {measurement} is not in valid range. MIN: {MIN}, MAX: {MAX}."
            logging.error(msg)
            return [False, msg, ApiResult.CONFLICT.value]

    msg = f"{measurement_type} measurement of {measurement} is in valid range. MIN: {MIN}, MAX: {MAX}."
    logging.info(msg)
    return [True, msg, ApiResult.SUCCESS.value]


def _open_json(json_file: str):  # -> List[bool, str, ApiResult, dictionary/json object]
    """This function opens a json file and returns the data as a dictionary"""

    try:
        with open(json_file, "r") as inFile:

            # check if json file has no content
            if os.path.getsize(json_file) == 0:
                msg = f"{json_file} is empty"
                logging.error(msg)
                return [False, msg, {}, ApiResult.DEFAULT_FAIL.value]

            # read in the entire json file
            data = json.load(inFile)
            msg = f"Successfully opened JSON file called: {json_file}"
            logging.info(msg)

            return [True, msg, data, ApiResult.SUCCESS.value]

    except IOError:
        openResult = f"Error:Sorry, the file {json_file} cannot be opened." \
                     f" Please check it exists in your directory."
        logging.error(openResult)
        data = {"msg": openResult}
        return [False, openResult, data, ApiResult.CONFLICT.value]


def _load_json_string(json_string: str):  # -> List[bool, str, ApiResult, json object]
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


def is_device_registered(device_id: int):  # -> List[bool, str., ApiResult]
    """This function checks if a device is registered.
    Returns true if the device is registered, otherwise false.
    Debugging message is also included.
    """
    msg = ""
    result = False
    api_result = ApiResult.DEFAULT_FAIL.value

    # check if device_id is an int
    if not isinstance(device_id, int):
        msg = f"Checking if device registered: device_id \"{device_id}\" is not an int."
        logging.error(msg)
        return [result, msg, ApiResult.CONFLICT.value]

    # get list of registered devices
    reg_devices = registered_devices["device_ids"]

    if device_id not in reg_devices:
        msg = f"is_device_registered: Device \"{device_id}\" is not registered."
        logging.info(msg)
        api_result = ApiResult.CONFLICT.value
    else:
        result = True
        msg = f"is_device_registered: Device \"{device_id}\" is registered."
        logging.info(msg)
        api_result = ApiResult.SUCCESS.value

    return [result, msg, api_result]


def register_device(device_id: int):  # -> List[bool, str]
    """This function registers a device.
    Returns true if the device is registers, otherwise false.
    Debugging message is also included.
    """

    msg = ""
    result = False

    # check if device_id is an int
    if not isinstance(device_id, int):
        msg = f"Registering Device: device_id \"{device_id}\" is not an int."
        logging.error(msg)
        return [result, msg, ApiResult.CONFLICT.value]

    is_device_registered_result = is_device_registered(device_id)

    # check if the device is already registered
    if is_device_registered_result[0]:
        msg = f"Registering Device: Device \"{device_id}\" is already registered."
        logging.error(msg)
        return [False, msg, ApiResult.CONFLICT.value]

    # write device to database
    writing_result = _edit_device_database(device_id, EditDevice.REGISTER)

    if not writing_result[0]:
        return writing_result

    # write to database successful
    result = True
    msg = f"Registering Device: Device \"{device_id}\" registered successfully."
    logging.info(msg)

    return [result, msg, ApiResult.SUCCESS.value]


def remove_device(device_id: int):  # -> List[bool, str]
    """This function removes device from database."""

    is_device_registered_result = is_device_registered(device_id)

    # check if the device is already registered
    if not is_device_registered_result[0]:
        msg = f"Removing Device: Device \"{device_id}\" is not registered. It can not be removed."
        logging.error(msg)
        return [False, msg, ApiResult.CONFLICT.value]

    # remove device from database
    remove_result = _edit_device_database(device_id, EditDevice.REMOVE)

    # check if the remove operation was successful
    if not remove_result[0]:
        return remove_result

    # remove operation was successful
    msg = f"Removing Device: Device \"{device_id}\" is successfully removed."
    logging.info(msg)
    return [True, msg, ApiResult.SUCCESS.value]


def _edit_device_database(device_id: int, operation: EditDevice):  # -> List[bool, str]
    """This function edits the device database.
       Operations include register, remove, update.
    """

    msg = ""
    editing_result = False

    # check if device_id is an int
    if not isinstance(device_id, int):
        msg = f"Editing Device Database: device_id \"{device_id}\" is not an int."
        logging.error(msg)
        return [False, msg, ApiResult.CONFLICT.value]

    # check if edit operation variable is of type EditDevice()
    if not isinstance(operation, EditDevice):
        msg = f"Editing Device Database: operation \"{operation}\" is not of type EditDevice"
        logging.error(msg)
        return [False, msg, ApiResult.CONFLICT.value]

    if operation == EditDevice.REGISTER:
        # add the device to the list of device_ids
        registered_devices["device_ids"].append(device_id)

        editing_result = device_id in registered_devices["device_ids"]

    elif operation == EditDevice.REMOVE:
        # remove the device from the list of device_ids
        registered_devices["device_ids"].remove(device_id)

        editing_result = device_id not in registered_devices["device_ids"]

    else:
        msg = f"Editing Device Database: operation \"{operation}\" is not currently supported."
        logging.error(msg)
        return [False, msg, ApiResult.CONFLICT.value]

    if not editing_result:
        msg = f"Editing Device Database: {operation.name} device_id \"{device_id}\" in the device database failed."
        logging.error(msg)
        return [False, msg, ApiResult.DEFAULT_FAIL.value]

    else:
        msg = f"Editing Device Database: {operation.name} device_id \"{device_id}\" in the device database successful."
        logging.info(msg)
        return [True, msg, ApiResult.SUCCESS.value]


def _write_json_file(file_name: str, json_data: dict):  # -> List[bool, str, ApiResult]
    """This function writes json data to a json file."""

    # check if file name passed is a string
    if not isinstance(file_name, str):
        msg = f"Writing to JSON file: file name \"{file_name}\" is not a string."
        logging.error(msg)
        return [False, msg, ApiResult.CONFLICT.value]

    # check if the file name has json extension
    is_json_file_result = _is_JSON_file(file_name)
    if not is_json_file_result[0]:
        return is_json_file_result

    # check if json data passed is a dictionary
    if not isinstance(json_data, dict):
        msg = "Writing to JSON file: json data passed is not a dictionary."
        logging.error(msg)
        return [False, msg, ApiResult.CONFLICT.value]

    try:
        with open(file_name, "w") as json_file:

            # read in the entire json file
            json.dump(json_data, json_file, indent=4)
            msg = f"Writing to JSON file: Successfully wrote to JSON file called: {file_name}"
            logging.info(msg)

            return [True, msg, ApiResult.SUCCESS.value]

    except IOError:
        openResult = f"Writing to JSON file: Sorry, the file \"{file_name}\" cannot be opened for writing."
        logging.error(openResult)
        return [False, openResult, ApiResult.NOT_FOUND.value]


if __name__ == '__main__':
    file = "data/tempJSON.json"
    # placeholder for testing device.py
    # print(send_measurements(file, passing_a_file=True))

    # print(verify_measurement_range("temperature", 98, "F"))
    # print(verify_measurement_range("temperature", 200, "F"))

    # print(register_device(123))
    # print(register_device(1))
    # print(remove_device(1))

    print(is_device_registered(1))
