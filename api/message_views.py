from flask import Blueprint, jsonify, json, request, abort
from .messages_model import Message, Received, messages
from .validations import Validate
from .user_views import token_required, created_token
from datetime import datetime
from .user_models import User

message = Blueprint('message', __name__)
validate = Validate()
senders = []


@message.route("/api/v1/messages", methods=["POST"])
@token_required
def new_message():
    """ Creates a new message"""
    data = request.get_json()
    message_id = len(messages)+1
    created_on = datetime.now()
    valid = validate.validate_message(data)
    try:
        if valid == "Valid":
            data["status"] = "sent"
            new_msg = Message(message_id, data["subject"], data["message"], created_on, data["status"])  
            messages.append(new_msg)
            return jsonify({
                "data": new_msg.__dict__
                }), 201
        return jsonify({"message": valid}), 400
    except ValueError:
        return jsonify({"message": "Invalid fields"})
    
