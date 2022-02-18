from flask import Flask
from flask_restful import Api, Resource
import jsonify
import device

app = Flask(__name__)
api = Api(app)

data_directory: str = "data/"


class ValidateJSON(Resource):
    def get(self, json_file):
        path: str = data_directory + json_file
        validate_result = device.validate_JSON(path)
        return {"result": validate_result[0],
                "message": validate_result[1],
                "path": path}


api.add_resource(ValidateJSON, "/device/validate/<string:json_file>", )

if __name__ == "__main__":
    app.run(debug=True)