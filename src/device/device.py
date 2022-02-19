from typing import List
from datetime import datetime
import logging
import json
import os


def send_measurements(json_file: str):  # -> List[bool, str]:
    """This function receives a JSON file and returns a list.
       The list index 0 indicates success of function and index 1 provides a status message"""

    # validate JSON file
    validate_JSON_format_results: List[bool, str] = validate_JSON(json_file)

    if not validate_JSON_format_results[0]:
        return validate_JSON_format_results

    # write json data to database
    json_data = validate_JSON_format_results[2]
    database_write_result = write_to_database(json_data)

    return database_write_result


def is_JSON_file(file: str):  # -> List[bool, str]:
    """Returns file type as string else it returns invalidFileName"""

    logging.info("Determining file type.")
    # print("Determining file type.")

    # checking if the argument passed is a string
    if isinstance(file, str):

        # tokenize the file string into file name and type
        fileName = file.split(".")

        # split returns list with only one element if delimiter not present in string
        if len(fileName) > 1:

            logging.info(f"User passed \"{file}\" as file name.")
            # print(f"User passed \"{file}\" as file name.")

            # extract the file type
            fileType = fileName[1]

            logging.info(f"The file extension is: {fileType}")
            # print(f"The file extension is: {fileType}")

            result: bool = fileType.lower() == "json"

            return [result, fileType]

        else:
            logging.info(f"\"{file}\" is not a valid file name")
            # print(f"\"{file}\" is not a valid file name")
            return [False, "invalidFileName"]


def validate_JSON(json_file: str):  # -> List[bool, str]:
    """This function checks that the json adheres to the device module's json schema"""

    is_JSON_file_results: List[bool, str] = is_JSON_file(json_file)

    # check that the file is a json
    if not is_JSON_file_results[0]:
        warning: str = "User did not pass a json file"
        logging.error(warning)
        return [False, warning]

    else:
        try:
            with open(json_file, "r") as inFile:

                # check if json file has no content
                if os.path.getsize(json_file) == 0:
                    msg = f"{json_file} is empty"
                    logging.error(msg)
                    return [False, msg]

                # read the entire json file
                data = json.load(inFile)

                # check primaryKeys
                primaryKeys = list(data.keys())
                primaryKeys_check_results = check_primary_keys(primaryKeys, data)

                if not primaryKeys_check_results[0]:
                    return primaryKeys_check_results

                # check measurementKeys
                measureKeys = list(data["measurements"].keys())
                measureKeys_check_results = check_measurement_keys(measureKeys, data)

                if not measureKeys_check_results[0]:
                    return measureKeys_check_results

                # check metadataKeys
                for key in measureKeys:
                    # pass the list of dictionaries
                    inner_data_list = data["measurements"][key]

                    # check metadata keys within the inner data packet
                    metadata_check_results = check_metadata_keys(key, inner_data_list)

                    if not metadata_check_results[0]:
                        return metadata_check_results

                # opening JSON file successful
                openResult = "JSON format is correct"

                return [True, openResult, data]

        except IOError:
            openResult = f"Error:Sorry, the file {json_file} cannot be opened." \
                         f" Please check it exists in your directory."

            logging.error(openResult)

            return [False, openResult]


def check_primary_keys(keys: List[str], json_data: json):  # -> List[bool, str]:
    primary_keys: List[str] = ["patientID", "deviceID", "deviceType", "measurements"]

    # check that json has four primary keys
    if len(keys) != len(primary_keys):
        return [False, "Missing primary keys"]

    # check that key only appears once
    for key in keys:
        key_occurrence = primary_keys.count(key)
        if key_occurrence != 1:
            return [False, f"incorrect key in data structure: {key} or it appears multiple times"]

    # at this point we have confirmed that each key from user file matches primary keys in schema
    # now we can use the primary keys to check the data types for each key/value pair
    # patientID: int, deviceID = int, deviceType: int, measurements: dict
    for key in primary_keys:
        if key == "measurements":
            if not isinstance(json_data[key], dict):
                msg = "measurements key does not have a dictionary assigned to it."
                logging.error(msg)
                return [False, msg]
        else:
            if not isinstance(json_data[key], int):
                msg = f"{key} key does not have an int value assigned to it."
                logging.error(msg)
                return [False, msg]

    # the primary keys and their respective value validate
    return [True, "all keys correct with corresponding value type"]


def check_measurement_keys(keys: List[str], json_data: json):  # -> List[bool, str]:
    """This function verifies the keys and values in measurements data structure"""

    # measure_key is the string for the name of the measurements key
    measure_key = "measurements"
    measurement_keys = ["temperature", "blood_pressure", "pulse", "oximeter",
                        "weight", "glucometer"]

    # check that key only appears once
    for key in keys:
        key_occurrence = measurement_keys.count(key)
        if key_occurrence != 1:
            msg = f"incorrect key in data structure: {key} or it appears multiple times"
            logging.error(msg)
            return [False, msg]

        # first index into measurements dictionary and then index by each key within the measurements dictionary
        # each measurement key needs to have a list
        if not isinstance(json_data[measure_key][key], list):
            msg = f"{key} key does not have a list value assigned to it."
            logging.error(msg)
            return [False, msg]

    # the measurement keys and their respective value validate
    return [True, "all measurement keys are valid and have an accompanying list"]


def check_metadata_keys(measurement_key: str, data: List[dict]):  # -> List[bool, str]:
    metadata_keys: List[str] = ["unit", "timestamp", "comments"]

    # each measurement_key will have a list that can contain
    # multiple inner dictionaries encapsulating the device's measurement data
    for data_dict in data:
        # grab the keys within the dictionary
        metaKeys = list(data_dict.keys())

        # measurement_key must be present in inner data packet
        measurement_key_occurrence = metaKeys.count(measurement_key)
        if measurement_key_occurrence != 1:
            msg = f"{measurement_key} measurement key is not in inner data packet."
            logging.error(msg)
            return [False, msg]

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
        verify_measurement_range_results = verify_measurement_range(measurement_key,measurement, unit)
        if not verify_measurement_range_results[0]:
            return verify_measurement_range_results

        # confirmed that measurement_key is in inner data packet, now can safely remove & continue checking other keys
        metaKeys.remove(measurement_key)

        # check that metadata keys only occur once within the inner data packet, and validate values
        for key in metaKeys:
            key_occurrence = metadata_keys.count(key)
            if key_occurrence != 1:
                logging.error("error is happening in check_metadata_keys")
                msg = f"key: {key}, key_occurrence: {key_occurrence}, it should only occur once"
                logging.error(msg)
                return [False, msg]

            # checking timestamp value
            if key == "timestamp":
                verify_timestamp_result = verify_timestamp(data_dict[key])

                if not verify_timestamp_result[0]:
                    return verify_timestamp_result

            # checking unit value
            elif key == "unit":
                verify_units_result = verify_units(measurement_key, data_dict[key])

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


def write_to_database(json_data: json):  # -> List[bool, str]:
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


def verify_units(measurement_key: str, unit: str):  # -> List[bool, str]
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


def verify_timestamp(timestamp: str):  # -> List[bool, str]
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


def verify_measurement_range(measurement_type: str, measurement, unit: str):  # -> List[bool, str]
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
    verify_units_result = verify_units(measurement_type, unit)
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


if __name__ == '__main__':
    file = "data/tempJSON.json"
    # placeholder for testing device.py
    # print(send_measurements(file))

    print(verify_measurement_range("temperature", 98, "F"))
    print(verify_measurement_range("temperature", 200, "F"))
