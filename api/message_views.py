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
    

@message.route('/api/v1/messages/<int:message_id>', methods=['GET'])
def fetch_single_message(message_id):
    fetched_message = []
    try:
        if validate.validate_id(message_id, messages):
            msg = messages[message_id - 1]
            fetched_message.append(msg.get_details())
            return jsonify({"Data": fetched_message}), 200
        return jsonify({"message": "Index out of range!"}), 400
    except IndexError:
        return "Index out of range", 400


@message.route('/api/v1/messages/<int:message_id>', methods=['DELETE'])
@token_required
def delete_message(message_id):
    if message_id == 0 or message_id > len(messages):
        return jsonify({"message": "Index out of range"}), 400
    for msg in messages:
        if msg.message_id == message_id:
            messages.remove(msg)
    return jsonify({"message": "message successfully removed"}), 200


@message.route("/api/v1/messages/received", methods=["GET"])
@token_required
def all_received_messages():
    received_id = len(received_messages)+1
    sender_id = len(senders)+1
    is_valid = validate.validate_message(data)
    if valid == "Valid":
        data["status"] = "received"
        Received_messages = [msg_received.get_all_received_messages for msg_received in messages] 
        return jsonify({"received_messages": Received_messages})