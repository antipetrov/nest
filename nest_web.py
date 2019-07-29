import os
import json
from functools import wraps

from flask import Flask, request, jsonify
from nesting.nest import make_nested_dicts, DictifyError, NestedError

app = Flask(__name__)
app.config['AUTH_ENABLED'] = os.getenv('NEST_WEB_AUTH_ENABLED', False)
app.config['AUTH_LOGIN'] = os.getenv('NEST_WEB_LOGIN')
app.config['AUTH_PASSWORD'] = os.getenv('NEST_WEB_PASSWORD')


def check_auth(login, password):
    return login == app.config['AUTH_LOGIN'] and password == app.config['AUTH_PASSWORD']


def auth_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):

        if app.config['AUTH_ENABLED']:
            if not request.authorization:
                return jsonify({'error': 'base-auth required'}), 401

            if not check_auth(request.authorization.username, request.authorization.password):
                resp = jsonify({'error': 'login or password invalid'})
                resp.status_code = 401
                resp.headers['WWW-Authenticate'] = 'Basic realm="Main"'
                return resp

        return func()

    return decorated


@app.route('/', methods=['POST'])
@auth_required
def nest():

    if not request.data:
        return jsonify({'error': 'no input list provided. json-list expected'}), 400

    try:
        input_data = json.loads(request.data)
    except json.JSONDecodeError:
        return jsonify({'error': 'invalid json'}), 400

    keys = request.args.get('keys').split(',') if 'keys' in request.args else None
    if not keys:
        return jsonify({'error': 'no nesting keys provided. GET-parameter named "keys" expected.'}), 400

    try:
        result = make_nested_dicts(input_data, keys)
    except (DictifyError, NestedError) as e:
        return jsonify({'error': str(e)}), 400

    return jsonify(result)


if __name__ == '__main__':

    debug_mode = os.getenv('NEST_DEBUG', True)
    app.run(debug=debug_mode)
