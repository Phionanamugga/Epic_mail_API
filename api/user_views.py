from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify, request, abort, Blueprint
from datetime import datetime, timedelta
from .validations import Validate
from .user_models import User
from functools import wraps
from config import Config
import jwt
import re

user = Blueprint('user', __name__)
users = []
created_token = []
validate = Validate()


def token_required(f): 
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
        if not token:
            return jsonify({"message": "Missing Token"}), 403
            jwt.decode(token, Config.SECRET_KEY)
        return f(*args, **kwargs)
    return decorated


@user.route('/api/v1/auth/signup', methods=['POST'])
def register_user():
    """ registers a user"""
    data = request.get_json()
    is_valid = validate.validate_user(data)
    for user in users:
        if user.email == data['email']:
            return jsonify({"message": "user already exists!"}), 400
    try:
        if is_valid == "is_valid":
            user_id = len(users)
            user_id += 1
            hashed_password = generate_password_hash(data['password'],
                                                     method='sha256')
            kwargs = {
                "user_id": user_id,
                "first_name": data['first_name'],
                "last_name": data['last_name'],
                "email": data['email'],
                "password": hashed_password,
              
            }
            user = User(**kwargs)
            users.append(user)
            return jsonify({"message":
                            "User registered successfully"}), 201
        return jsonify({"message": is_valid}), 400
    except KeyError:
        return "Invalid key fields"


@user.route('/api/v1/auth/login', methods=['POST'])
def login():
    """Logs in a user"""
    data = request.get_json()
    try:
        email = data['email']
        is_valid = validate.validate_login(data)
        if re.match(r"([\w\.-]+)@([\w\.-]+)(\.[\w\.]+$)", email) and\
           is_valid == "Credentials valid":
            return assigns_token(data)
        return jsonify({"message": is_valid}), 400
    except KeyError:
        return jsonify({"message": "Invalid keys"}), 400


def assigns_token(data):
    for item in users:
        if item.email == data['email'] and\
           check_password_hash(item.password, data['password']):
                token = jwt.encode({'user': item.user_id,
                                    'exp': datetime.utcnow() +
                                    timedelta(minutes=30)},
                                   Config.SECRET_KEY)
                return jsonify({'token': token.decode('UTF-8')}), 200
    return jsonify({
        "message": "User either not registered or forgot password"}), 400
    
