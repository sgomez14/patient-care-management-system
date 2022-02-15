import device
import json


def simulate_send_measurements(json_file: str):  # -> List[bool, str]

    results = device.send_measurements(json_file)

    return results


def simulate_validate_JSON(json_file: str):  # -> List[bool, str]

    results = device.validate_JSON(json_file)

    return results


if __name__ == '__main__':
    file1 = "data/tempJSON.json"
    file2 = "data/temp_bp.json"
    database_file = "data/database.json"
    inputData = ""
    databaseData = ""

    with open(file2, "r") as inFile:
        inputData = json.load(inFile)

    results = simulate_validate_JSON(file2)

    if results[0]:
        results = simulate_send_measurements(file2)

        if results[0]:
            with open(database_file, "r") as database:
                databaseData = json.load(database)

            inputData_database_are_equal = (inputData == databaseData)

            print(f"Are inputData and databaseData equal: {inputData_database_are_equal}")
    else:
        print(f"JSON file {file2} failed to validate")
