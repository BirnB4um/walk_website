
from flask import Flask, Blueprint, request

bp_api = Blueprint('api', __name__)


@bp_api.route('/sayhello', methods=['POST'])
def sayhello():
    print(request.json)
    return 'Hello, World!'

