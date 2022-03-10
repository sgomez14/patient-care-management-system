# import sys
# sys.path.append("..")

from flask import Flask  # ,jsonify
from flask_restful import Api, Resource, abort
from src.device import device

application = Flask(__name__)
# app = application
api = Api(application, catch_all_404s=True)

data_directory: str = "data/"


def error_handler(error_code: int, msg: str) -> None:
    abort(error_code, msg)


class HomePage(Resource):
    def get(self):

        return "Landing page for Device Module API"


class ValidateJSON(Resource):
    def get(self, json_file):
        validate_result = device.validate_JSON(json_file)
        return {"result": validate_result[0],
                "message": validate_result[1],
                "data": json_file}


class SendMeasurements(Resource):
    def get(self, json_file):
        send_measurements_result = device.validate_JSON(json_file)
        return {"result": send_measurements_result[0],
                "message": send_measurements_result[1],
                "data": json_file}

    def post(self, json_file):
        send_measurements_result = device.send_measurements(json_file)
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
        return {"result": registered_result[0],
                "message": registered_result[1],
                "device_id": device_id}


class RemoveDevice(Resource):
    def put(self, device_id):
        registered_result = device.remove_device(device_id)
        msg = registered_result[1]

        if not registered_result[0]:
            error_handler(409,msg)
            
        return {"result": registered_result[0],
                "message": registered_result[1],
                "device_id": device_id}


api.add_resource(HomePage, "/")
api.add_resource(ValidateJSON, "/device/validate/<string:json_file>")
api.add_resource(SendMeasurements, "/device/send-measurements/<string:json_file>")
api.add_resource(IsDeviceRegistered, "/device/is-device-registered/<int:device_id>")
api.add_resource(RegisterDevice, "/device/register-device/<int:device_id>")
api.add_resource(RemoveDevice, "/device/remove-device/<int:device_id>")

if __name__ == "__main__":
    application.run(debug=True)