from flask import Flask, redirect
from api.user_views import user
from api.message_views import message

app = Flask(__name__)
app.register_blueprint(message)
app.register_blueprint(user)