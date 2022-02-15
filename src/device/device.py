from typing import List
import logging
import json

database: str = "data/database.json"


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


# returns file type as string else it returns "invalidFileName"
def is_JSON_file(file: str):  # -> List[bool, str]:

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

    is_JSON_file_results: List[bool, str] = is_JSON_file(json_file)

    # check that the file is a json
    if not is_JSON_file_results[0]:
        warning: str = "User did not pass a json file"
        logging.error(warning)
        return [False, warning]

    else:
        try:
            with open(json_file, "r") as inFile:
                # read the entire json file
                data = json.load(inFile)

                # check primaryKeys
                primaryKeys = list(data.keys())
                primaryKeys_check_results = check_primary_keys(primaryKeys)

                if not primaryKeys_check_results[0]:
                    return primaryKeys_check_results

                # check measurementKeys
                measureKeys = list(data["measurements"].keys())
                measureKeys_check_results = check_measurement_keys(measureKeys)

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


def check_primary_keys(keys: List[str]):  # -> List[bool, str]:
    primary_keys = ["patientID", "deviceID", "deviceType", "measurements"]

    # check that json has four primary keys
    if len(keys) != len(primary_keys):
        return [False, "Missing primary keys"]

    # check that key only appears once
    for key in keys:
        key_occurrence = primary_keys.count(key)
        if key_occurrence != 1:
            return [False, f"incorrect key in data structure: {key} or it appears multiple times"]

    return [True, "all keys correct"]


def check_measurement_keys(keys: List[str]):  # -> List[bool, str]:
    """This function verifies the keys and values in measurements data structure"""
    measurement_keys = ["temperature", "blood_pressure", "pulse", "oximeter",
                        "weight", "glucometer"]

    # check that key only appears once
    for key in keys:
        key_occurrence = measurement_keys.count(key)
        if key_occurrence != 1:
            logging.error("error is happening in check_measurement_keys")
            return [False, f"incorrect key in data structure: {key} or it appears multiple times"]

    return [True, "all keys correct"]


def check_metadata_keys(measurement_key: str, data: List[dict]):  # -> List[bool, str]:
    metadata_keys = ["unit", "timestamp", "comments"]

    for data_dict in data:
        metaKeys = list(data_dict.keys())
        measurement_key_occurrence = metaKeys.count(measurement_key)

        # measurement_key must be present in inner data packet
        if measurement_key_occurrence != 1:
            return [False, "measurement key is not in inner data packet"]

        # confirmed that measurement_key is in inner data packet, now can safely remove & continue checking other keys
        metaKeys.remove(measurement_key)

        # check that metadata keys only occur once within the inner data packet
        for key in metaKeys:
            key_occurrence = metadata_keys.count(key)
            if key_occurrence != 1:
                logging.error("error is happening in check_metadata_keys")
                logging.error(f"key: {key}, key_occurrence: {key_occurrence}")
                return [False, f"incorrect key in data structure: {key} or it appears multiple times"]

    message = "Inner data keys validated"
    logging.info(message)
    return [True, message]


def write_to_database(json_data: json):  # -> List[bool, str]:
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


if __name__ == '__main__':
    file = "data/tempJSON.json"
    # placeholder for testing device.py
    print(send_measurements(file))
