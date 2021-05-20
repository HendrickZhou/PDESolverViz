from flask import Flask, jsonify, request
from flask_cors import CORS

import sys, os
cur_path = os.getcwd()
server_path = cur_path[:cur_path.find("server")+7]
pack_path = server_path + 'transpiler'
sys.path.insert(0, pack_path)

from equations import PoissonTranslator
from geo_script import Transpiler
import deepxde as dde

import json


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
    c = Transpiler(code_data)
    xde_obj_dicts, json_stream = c.run()
    print(json_stream)
    # build xde model, lazy loading

    # transmit json file
    # mock the project id 
    import datetime
    script_name = str(datetime.datetime.now()) + '.json'
    with open('./cache/' + script_name, 'w') as f:
        json.dump(json_stream, f, indent=2)
    
    return {"prompt" : str(xde_obj_dicts)}


if __name__ == '__main__':
    app.run()