from flask import Flask, Response
from flask_restful import Api, Resource, abort
from src.device import device
from src.chat import chat, chat_utils
from src.users.users import authenticate_login, get_user_assignments, get_patient_summary

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

        return "Landing page for the Patient Care Management System API"



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


class ValidateChatPacket(Resource):
    def get(self, chat_json):

        validate_result = chat.validate_message_packet(chat_json)

        if api_call_successful(operation_success=validate_result[0],
                               msg=validate_result[1],
                               error_code=validate_result[2]):

            chat_packet = validate_result[-1]
            access_token = chat_packet["api_access_token"]

            # block to verify access_token
            verify_token_result = chat.verify_chat_token(access_token)

            if api_call_successful(operation_success=verify_token_result[0],
                                   msg=verify_token_result[1],
                                   error_code=verify_token_result[2]):
                return {"result": validate_result[0],
                        "message": validate_result[1],
                        "data_validated": chat_packet}


class GetChatByMessageID(Resource):
    def get(self, token_and_id_json):

        json_load_results = chat_utils.load_json_string(token_and_id_json)

        if api_call_successful(operation_success=json_load_results[0],
                               msg=json_load_results[1],
                               error_code=json_load_results[3]):

            token_id_pair = json_load_results[2]
            access_token = token_id_pair["api_access_token"]

            # block to verify access_token
            verify_token_result = chat.verify_chat_token(access_token)

            if api_call_successful(operation_success=verify_token_result[0],
                                   msg=verify_token_result[1],
                                   error_code=verify_token_result[2]):

                message_id = token_id_pair["message_id"]

                query_result = chat.ChatDB.find_by_message_id(message_id)

                return {"result": query_result[0],
                        "message": query_result[1],
                        "data": query_result[-1]}


class GetChatBySessionID(Resource):
    def get(self, token_and_id_json):

        json_load_results = chat_utils.load_json_string(token_and_id_json)

        if api_call_successful(operation_success=json_load_results[0],
                               msg=json_load_results[1],
                               error_code=json_load_results[3]):

            token_id_pair = json_load_results[2]
            access_token = token_id_pair["api_access_token"]

            # block to verify access_token
            verify_token_result = chat.verify_chat_token(access_token)

            if api_call_successful(operation_success=verify_token_result[0],
                                   msg=verify_token_result[1],
                                   error_code=verify_token_result[2]):

                session_id = token_id_pair["session_id"]

                query_result = chat.ChatDB.find_by_session_id(session_id)

                return {"result": query_result[0],
                        "message": query_result[1],
                        "data": query_result[-1]}


class GetChatByMessageOwner(Resource):
    def get(self, token_and_id_json):

        json_load_results = chat_utils.load_json_string(token_and_id_json)

        if api_call_successful(operation_success=json_load_results[0],
                               msg=json_load_results[1],
                               error_code=json_load_results[3]):

            token_id_pair = json_load_results[2]
            access_token = token_id_pair["api_access_token"]

            # block to verify access_token
            verify_token_result = chat.verify_chat_token(access_token)

            if api_call_successful(operation_success=verify_token_result[0],
                                   msg=verify_token_result[1],
                                   error_code=verify_token_result[2]):

                message_owner = token_id_pair["message_owner"]

                query_result = chat.ChatDB.find_by_message_owner(message_owner)

                return {"result": query_result[0],
                        "message": query_result[1],
                        "data": query_result[-1]}


class StoreChat(Resource):
    def post(self, chat_packet):

        json_load_results = chat_utils.load_json_string(chat_packet)

        if api_call_successful(operation_success=json_load_results[0],
                               msg=json_load_results[1],
                               error_code=json_load_results[3]):

            chat_packet = json_load_results[2]
            access_token = chat_packet["api_access_token"]

            # block to verify access_token
            verify_token_result = chat.verify_chat_token(access_token)

            if api_call_successful(operation_success=verify_token_result[0],
                                   msg=verify_token_result[1],
                                   error_code=verify_token_result[2]):

                post_result = chat.ChatDB.post_document(chat_packet)

                return {"result": post_result[0],
                        "message": post_result[1],
                        "code": post_result[-1]}


# user module section

class AuthenticateLogin(Resource):
    def get(self, login_json):

        authenticate_result = authenticate_login(login_json)

        if api_call_successful(operation_success=authenticate_result[0],
                               msg=authenticate_result[1],
                               error_code=authenticate_result[2]):

            return {"result": authenticate_result[0],
                    "message": authenticate_result[1],
                    "http_code": authenticate_result[2],
                    "user_roles": authenticate_result[-1]}


class GetUserAssignments(Resource):
    def get(self, user_id):
        assignments_result = get_user_assignments(user_id)

        if api_call_successful(operation_success=assignments_result[0],
                               msg=assignments_result[1],
                               error_code=assignments_result[2]):
            return {"result":     assignments_result[0],
                    "message":    assignments_result[1],
                    "http_code":  assignments_result[2],
                    "assignments": assignments_result[-1]}


class GetPatientSummary(Resource):
    def get(self, user_id):
        summary_result = get_patient_summary(user_id)

        if api_call_successful(operation_success=summary_result[0],
                               msg=summary_result[1],
                               error_code=summary_result[2]):
            return {"result": summary_result[0],
                    "message": summary_result[1],
                    "http_code": summary_result[2],
                    "summary": summary_result[-1]}


# All API endpoints
api.add_resource(HomePage, "/")

# endpoints for device module
api.add_resource(ValidateJSON, "/device/validate/<string:json_file>")
api.add_resource(SendMeasurements, "/device/send-measurements/<string:json_file>")
api.add_resource(IsDeviceRegistered, "/device/is-device-registered/<int:device_id>")
api.add_resource(RegisterDevice, "/device/register-device/<int:device_id>")
api.add_resource(RemoveDevice, "/device/remove-device/<int:device_id>")

# endpoints for chat module
api.add_resource(ValidateChatPacket, "/chat/validate-chat-packet/<string:chat_json>")
api.add_resource(GetChatByMessageID, "/chat/get-chat-by-message-id/<string:token_and_id_json>")
api.add_resource(GetChatBySessionID, "/chat/get-chat-by-session-id/<string:token_and_id_json>")
api.add_resource(GetChatByMessageOwner, "/chat/get-chat-by-message-owner/<string:token_and_id_json>")
api.add_resource(StoreChat, "/chat/store-chat/<string:chat_packet>")

# endpoints for users module
api.add_resource(AuthenticateLogin, "/users/authenticate-login/<string:login_json>")
api.add_resource(GetUserAssignments, "/users/get-assignments/<int:user_id>")
api.add_resource(GetPatientSummary, "/users/get-patient-summary/<int:user_id>")

if __name__ == "__main__":
    application.run(debug=True, use_debugger=True)
