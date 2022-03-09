from typing import List
from datetime import datetime
import logging
import json
import os
import enum


def send_measurements(json_file: str, flask_path=False, passing_a_file=False):  # -> List[bool, str]:
    """This function receives a JSON file and returns a list.
       The list index 0 indicates success of function and index 1 provides a status message"""

    # validate JSON file
    validate_JSON_format_results: List[bool, str] = validate_JSON(json_file, flask_path=flask_path, passing_a_file=passing_a_file)

    if not validate_JSON_format_results[0]:
        return validate_JSON_format_results

    # write json data to database
    json_data = validate_JSON_format_results[2]
    database_write_result = _write_to_database(json_data)

    return database_write_result


def _is_JSON_file(file: str):  # -> List[bool, str]:
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

            return [result, msg]

        else:
            msg = f"invalidFileName: \"{file}\" is not a valid file name"
            logging.error(msg)
            return [False, msg]


def validate_JSON(json_file: str, flask_path=False, passing_a_file=False):  # -> List[bool, str]:
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
            return [False, warning]

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
            msg = f"{load_json_string_results[1]} | validate_json: Received error loading json string"
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
    if flask_path != 0:
        check_device_registered_result = is_device_registered(data["deviceID"], flask_path)
    else:
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

    return [True, openResult, data]


def _check_primary_keys(keys: List[str], json_data: json):  # -> List[bool, str]:
    primary_keys: List[str] = ["patientID", "deviceID", "deviceType", "measurements"]

    # check that json has four primary keys
    if len(keys) != len(primary_keys):
        msg = "Missing primary keys"
        logging.error(msg)
        return [False, msg]

    # check that key only appears once
    for key in keys:
        key_occurrence = primary_keys.count(key)
        if key_occurrence != 1:
            msg = f"incorrect key in data structure: \"{key}\" or it appears multiple times"
            logging.error(msg)
            return [False, msg]

    # at this point we have confirmed that each key from user file matches primary keys in schema
    # now we can use the primary keys to check the data types for each key/value pair
    # patientID: int, deviceID = int, deviceType: int, measurements: dict
    for key in primary_keys:
        if key == "measurements":
            if not isinstance(json_data[key], dict):
                msg = f"measurements key does not have a dictionary assigned to it. Value provided: {json_data[key]}"
                logging.error(msg)
                return [False, msg]

            if len(json_data[key]) == 0:
                msg = f"measurements key's dictionary is empty. Value provided: {json_data[key]}"
                logging.error(msg)
                return [False, msg]
        else:
            if not isinstance(json_data[key], int):
                msg = f"{key} key does not have an int value assigned to it. Value provided: {json_data[key]}"
                logging.error(msg)
                return [False, msg]

    # the primary keys and their respective value validate
    return [True, "all keys correct with corresponding value type"]


def _check_measurement_keys(keys: List[str], json_data: json):  # -> List[bool, str]:
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
            return [False, msg]

        # first index into measurements dictionary and then index by each key within the measurements dictionary
        # each measurement key needs to have a list
        if not isinstance(json_data[measure_key][key], list):
            msg = f"{key} key does not have a list value assigned to it. Value provided: {json_data[measure_key][key]}"
            logging.error(msg)
            return [False, msg]

        # check that list is not empty
        if len(json_data[measure_key][key]) == 0:
            msg = f"{key} key has an empty list assigned to it. Value provided: {json_data[measure_key][key]}"
            logging.error(msg)
            return [False, msg]

    # the measurement keys and their respective value validate
    return [True, "all measurement keys are valid and have an accompanying list"]


def _check_metadata_keys(measurement_key: str, data: List[dict]):  # -> List[bool, str]:
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
            return [False, msg]

        # measurement_key must be present in inner data packet
        measurement_key_occurrence = metaKeys.count(measurement_key)
        if measurement_key_occurrence != 1:
            msg = f"{measurement_key} measurement key is not in inner data packet."
            logging.error(msg)
            return [False, msg]

        # remove measurement_key temporarily to check metadata_keys are correct
        metaKeys.remove(measurement_key)
        for key in metaKeys:
            key_occurrence = metadata_keys.count(key)
            if key_occurrence != 1:
                logging.error("error is happening in check_metadata_keys")
                msg = f"key: {key}, key_occurrence: {key_occurrence}, it must once, or this key is not supported." \
                      f"supported metadata_keys are: {metadata_keys}"
                logging.error(msg)
                return [False, msg]

        # reinsert measurement key into list
        metaKeys.append(measurement_key)

        # check that keys for blood_pressure dictionary are named systolic and diastolic
        if measurement_key == "blood_pressure":
            # blood pressure dictionary must have two keys: systolic and diastolic
            elements_in_blood_pressure_dict: int = 2

            if len(data_dict[measurement_key]) != elements_in_blood_pressure_dict:
                msg = f"there are not enough keys in the {measurement_key} dictionary"
                logging.error(msg)
                return [False, msg]

            for key in data_dict[measurement_key].keys():
                # check that keys are either systolic or diastolic
                if key != "systolic" and key != "diastolic":
                    msg = f"{key} key in the {measurement_key} dictionary is not named systolic or diastolic"
                    logging.error(msg)
                    return [False, msg]

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
                    return [False, msg]

    msg = "Inner data keys and values validated"
    logging.info(msg)
    return [True, msg]


def _write_to_database(json_data: json):  # -> List[bool, str]:
    database: str = "data/database.json"
    try:
        with open(database, "w") as json_file:
            json.dump(json_data, json_file, indent=4)

        message = "JSON data successfully written to database"
        logging.info(message)
        return [True, message]

    except IOError:
        message = "Could not write json data to database"
        logging.error(message)

        return [False, message]


def _verify_units(measurement_key: str, unit: str):  # -> List[bool, str]
    supported_measurements = ["temperature", "blood_pressure", "pulse", "oximeter",
                              "weight", "glucometer"]

    supported_units = {"temperature": ["F", "C"], "blood_pressure": "mmHg", "pulse": "bpm", "oximeter": "%",
                       "weight": ["lbs", "kg"], "glucometer": "mg/dl"}

    result: bool = False

    if measurement_key not in supported_measurements:
        msg = f"{measurement_key} is not a supported measurement key"
        logging.error(msg)
        return [False, msg]

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
        return [True, msg]
    else:
        msg = f"{unit} unit is not valid unit for {measurement_key}."
        logging.error(msg)
        return [False, msg]


def _verify_timestamp(timestamp: str):  # -> List[bool, str]
    """This function verifies that timestamp adheres to ISO 8601 standard"""

    iso8601_format: str = "%Y-%m-%dT%H:%M:%S"

    if not isinstance(timestamp, str):
        msg = f"{timestamp} timestamp must be a string"
        logging.error(msg)
        return [False, msg]

    try:
        if datetime.strptime(timestamp, iso8601_format):
            msg = f"{timestamp} timestamp validated."
            logging.info(msg)
            return [True, msg]

        else:
            msg = f"provided timestamp {timestamp} does not adhere to ISO8601 standard," \
                  f" eg. 1991-10-28T01:30:58"
            logging.error(msg)
            return [False, msg]
    except ValueError:
        msg = f"provided timestamp {timestamp} does not adhere to ISO8601 standard," \
              f" eg. 1991-10-28T01:30:58"
        logging.error(msg)
        return [False, msg]


def _verify_measurement_range(measurement_type: str, measurement, unit: str):  # -> List[bool, str]
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
        return [False, msg]

    # check the measurement_type is supported, the count must equal 1 to indicate that measurement_type is supported
    if list(supported.keys()).count(measurement_type) != 1:
        msg = f"Passed {measurement_type} as a measurement_type, but it is not supported." \
              f"Supported measurement types are {list(supported.keys())}"
        logging.error(msg)
        return [False, msg]

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
            return [False, msg]

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
            return [False, msg]

        if diastolic_reading < MIN_DIASTOLIC or diastolic_reading > MAX_DIASTOLIC:
            msg = f"{measurement_type} measurement of {measurement} is not in valid range." \
                  f" MIN: {supported[measurement_type][min_bp]}, MAX: {supported[measurement_type][max_bp]}."
            logging.error(msg)
            return [False, msg]

    else:
        if measurement < MIN or measurement > MAX:
            msg = f"{measurement_type} measurement of {measurement} is not in valid range. MIN: {MIN}, MAX: {MAX}."
            logging.error(msg)
            return [False, msg]

    msg = f"{measurement_type} measurement of {measurement} is in valid range. MIN: {MIN}, MAX: {MAX}."
    logging.info(msg)
    return [True, msg]


def _open_json(json_file: str):  # -> List[bool, str, dictionary/json object]
    """This function opens a json file and returns the data as a dictionary"""

    try:
        with open(json_file, "r") as inFile:

            # check if json file has no content
            if os.path.getsize(json_file) == 0:
                msg = f"{json_file} is empty"
                logging.error(msg)
                return [False, msg]

            # read in the entire json file
            data = json.load(inFile)
            msg = f"Successfully opened JSON file called: {json_file}"
            logging.info(msg)

            return [True, msg, data]

    except IOError:
        openResult = f"Error:Sorry, the file {json_file} cannot be opened." \
                     f" Please check it exists in your directory."
        logging.error(openResult)
        data = {"msg": openResult}
        return [False, openResult, data]


def _load_json_string(json_string: str):  # -> List[bool, str, json object]
    """This function loads json from a string"""

    # helper code from Kite.com
    # https://www.kite.com/python/answers/how-to-handle-json-decode-error-when-nothing-returns-in-python

    try:
        data = json.loads(json_string)
        msg = f"_load_json_string: Successfully loaded JSON string called: {json_string}"
        logging.info(msg)
        return [True, msg, data]

    except json.decoder.JSONDecodeError:
        data = {}
        msg = "_load_json_string: String could not be converted to JSON"
        logging.error(msg)
        return [False, msg, data]


# Using enums
# https://www.geeksforgeeks.org/enum-in-python/
class EditDevice(enum.Enum):
    REGISTER = 0
    UPDATE = 1
    REMOVE = 2


def is_device_registered(device_id: int, flask_path=False):  # -> List[bool, str]
    """This function checks if a device is registered.
    Returns true if the device is registered, otherwise false.
    Debugging message is also included.
    """
    msg = ""
    result = False

    # check if device_id is an int
    if not isinstance(device_id, int):
        msg = f"Checking if device registered: device_id \"{device_id}\" is not an int."
        logging.error(msg)
        return [result, msg]

    database = "data/registered_devices.json"

    if flask_path:
        database = os.path.join(flask_path, "src", "device", "data", "registered_devices.json")

    # connect to database, which is a json at this stage in module development
    json_open_results = _open_json(database)

    # check if the open did not work
    if not json_open_results[0]:
        return json_open_results

    # the json data is the 3 element in the list returned by open_json
    # the json has the device IDs in a list that is paired to key "device_ids"
    registered_devices = json_open_results[2]["device_ids"]

    if device_id not in registered_devices:
        msg = f"Checking device registration: Device \"{device_id}\" is not registered."
        logging.info(msg)
    else:
        result = True
        msg = f"Checking device registration: Device \"{device_id}\" is registered."
        logging.info(msg)

    return [result, msg]


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
        return [result, msg]

    is_device_registered_result = is_device_registered(device_id)
    total_result_items = len(is_device_registered_result)

    # failing due to file IO can be detected if the total items in the result is greater than 2
    reg_check_failed_due_to_fileIO = total_result_items > 2

    # check if the device check failed due to file IO
    if not is_device_registered_result[0] and reg_check_failed_due_to_fileIO:
        return is_device_registered_result

    # check if the device is already registered
    elif is_device_registered_result[0]:
        msg = f"Registering Device: Device \"{device_id}\" is already registered."
        logging.error(msg)
        return [False, msg]

    # write device to database
    writing_result = _edit_device_database(device_id, EditDevice.REGISTER)

    if not writing_result[0]:
        return writing_result

    # write to database successful
    result = True
    msg = f"Registering Device: Device \"{device_id}\" registered successfully."
    logging.info(msg)

    return [result, msg]


def remove_device(device_id: int):  # -> List[bool, str]
    """This function removes device from database."""

    is_device_registered_result = is_device_registered(device_id)
    total_result_items = len(is_device_registered_result)

    # failing due to file IO can be detected if the total items in the result is greater than 2
    reg_check_failed_due_to_fileIO = total_result_items > 2

    # check if the device check failed due to file IO
    if not is_device_registered_result[0] and reg_check_failed_due_to_fileIO:
        return is_device_registered_result

    # check if the device is already registered
    elif not is_device_registered_result[0] and not reg_check_failed_due_to_fileIO:
        msg = f"Removing Device: Device \"{device_id}\" is not registered."
        logging.error(msg)
        return [False, msg]

    # remove device from database
    remove_result = _edit_device_database(device_id, EditDevice.REMOVE)

    # check if the remove operation was successful
    if not remove_result[0]:
        return remove_result

    # remove operation was successful
    msg = f"Removing Device: Device \"{device_id}\" is successfully removed."
    logging.info(msg)
    return [True, msg]


def _edit_device_database(device_id: int, operation: EditDevice):  # -> List[bool, str]
    """This function edits the device database.
       Operations include register, remove, update.
    """

    msg = ""
    database = "data/registered_devices.json"

    # connect to database, which is a json at this stage in module development
    json_open_results = _open_json(database)

    # check if the json file opened corrected
    if not json_open_results[0]:
        return json_open_results

    # check if device_id is an int
    if not isinstance(device_id, int):
        msg = f"Editing Device Database: device_id \"{device_id}\" is not an int."
        logging.error(msg)
        return [False, msg]

    # check if edit operation variable is of type EditDevice()
    if not isinstance(operation, EditDevice):
        msg = f"Editing Device Database: operation \"{operation}\" is not of type EditDevice"
        logging.error(msg)
        return [False, msg]

    # grab the json with the device info
    devices = json_open_results[2]

    if operation == EditDevice.REGISTER:
        # add the device to the list of device_ids
        devices["device_ids"].append(device_id)

    elif operation == EditDevice.REMOVE:
        # remove the device from the list of device_ids
        devices["device_ids"].remove(device_id)

    else:
        msg = f"Editing Device Database: operation \"{operation}\" is not currently supported."
        logging.error(msg)
        return [False, msg]

    # update number of devices
    devices["total_devices"] = len(devices["device_ids"])

    # write to database
    writing_result = _write_json_file(database, devices)

    if not writing_result[0]:
        msg = f"Editing Device Database: {operation.name} device_id \"{device_id}\" in the device database failed."
        logging.error(msg)
        return [False, msg]

    else:
        msg = f"Editing Device Database: {operation.name} device_id \"{device_id}\" in the device database successful."
        logging.info(msg)
        return [True, msg]


def _write_json_file(file_name: str, json_data: dict):  # -> List[bool, str]
    """This function writes json data to a json file."""

    # check if file name passed is a string
    # if not isinstance(file_name, str):
    #     msg = f"Writing to JSON file: file name \"{file_name}\" is not a string."
    #     logging.error(msg)
    #     return [False, msg]

    is_json_file_result = _is_JSON_file(file_name)
    if not is_json_file_result[0]:
        return is_json_file_result

    # check if json data passed is a dictionary
    if not isinstance(json_data, dict):
        msg = "Writing to JSON file: json data passed is not a dictionary."
        logging.error(msg)
        return [False, msg]

    try:
        with open(file_name, "w") as json_file:

            # read in the entire json file
            json.dump(json_data, json_file, indent=4)
            msg = f"Writing to JSON file: Successfully wrote to JSON file called: {file_name}"
            logging.info(msg)

            return [True, msg]

    except IOError:
        openResult = f"Writing to JSON file: Sorry, the file \"{file_name}\" cannot be opened for writing."
        logging.error(openResult)
        return [False, openResult]


if __name__ == '__main__':
    file = "data/tempJSON.json"
    # placeholder for testing device.py
    print(send_measurements(file, passing_a_file=True))

    # print(verify_measurement_range("temperature", 98, "F"))
    # print(verify_measurement_range("temperature", 200, "F"))

    # print(register_device(123))
    # print(register_device(1))
    # print(remove_device(1))