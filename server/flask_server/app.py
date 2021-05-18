from flask import Flask, jsonify, request
from flask_cors import CORS

import sys, os
cur_path = os.getcwd()
server_path = cur_path[:cur_path.find("server")+7]
pack_path = server_path + 'transpiler'
sys.path.insert(0, pack_path)

from equations import PoissonTranslator
from geo_script import _Context
import deepxde as dde


# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


@app.route('/submitCode', methods=['POST'])
def getCode():
    if request.is_json:
        code_data = request.get_json()['code']
    else:
        code_data = None
    print(code_data)
    c = _Context(code_data)
    c.run()
    return jsonify('pong!')


if __name__ == '__main__':
    app.run()