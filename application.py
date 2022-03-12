# import sys
# sys.path.append("..")

from flask import Flask, Response  # ,jsonify
from flask_restful import Api, Resource, abort
from src.device import device

application = Flask(__name__)
# app = application
api = Api(application, catch_all_404s=True)

data_directory: str = "data/"


def error_handler(error_code: int, error_msg: str) -> None:
    """This function calls abort with the error code passed and custom message"""

    abort(Response(error_msg, error_code))


def api_call_successful(operation_success: bool, msg: str, error_code: int) -> bool:
    """This function checks if the API call succeeded.
     Returns True if successful, otherwise calls error_handler.
     """

    if operation_success:
        return True
    else:
        error_handler(error_code=error_code, error_msg=msg)
        return False


class HomePage(Resource):
    def get(self):
        return "Landing page for Device Module API"


class ValidateJSON(Resource):
    def get(self, json_file):
        validate_result = device.validate_JSON(json_file)

        if api_call_successful(operation_success=validate_result[0],
                               msg=validate_result[1],
                               error_code=validate_result[2]):

            return {"result": validate_result[0],
                    "message": validate_result[1],
                    "data": json_file}


class SendMeasurements(Resource):
    # def get(self, json_file):
    #     send_measurements_result = device.validate_JSON(json_file)
    #     return {"result": send_measurements_result[0],
    #             "message": send_measurements_result[1],
    #             "data": json_file}

    def post(self, json_file):
        send_measurements_result = device.send_measurements(json_file)

        if api_call_successful(operation_success=send_measurements_result[0],
                               msg=send_measurements_result[1],
                               error_code=send_measurements_result[2]):

            return {"result": send_measurements_result[0],
                    "message": send_measurements_result[1],
                    "data": json_file}


class IsDeviceRegistered(Resource):
    def get(self, device_id):
        registered_result = device.is_device_registered(device_id)
        return {"result": registered_result[0],
                "message": registered_result[1],
                "device_id": device_id}


class RegisterDevice(Resource):
    def post(self, device_id):
        registered_result = device.register_device(device_id)

        if api_call_successful(operation_success=registered_result[0],
                               msg=registered_result[1],
                               error_code=registered_result[2]):

            return {"result": registered_result[0],
                    "message": registered_result[1],
                    "device_id": device_id}


class RemoveDevice(Resource):
    def put(self, device_id):
        remove_result = device.remove_device(device_id)

        if api_call_successful(operation_success=remove_result[0],
                               msg=remove_result[1],
                               error_code=remove_result[2]):

            return {"result": remove_result[0],
                    "message": remove_result[1],
                    "device_id": device_id}


api.add_resource(HomePage, "/")
api.add_resource(ValidateJSON, "/device/validate/<string:json_file>")
api.add_resource(SendMeasurements, "/device/send-measurements/<string:json_file>")
api.add_resource(IsDeviceRegistered, "/device/is-device-registered/<int:device_id>")
api.add_resource(RegisterDevice, "/device/register-device/<int:device_id>")
api.add_resource(RemoveDevice, "/device/remove-device/<int:device_id>")

if __name__ == "__main__":
    application.run(debug=True)
