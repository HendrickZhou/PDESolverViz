from flask import Flask, jsonify, request
from flask_cors import CORS

import sys, os
cur_path = os.getcwd()
server_path = cur_path[:cur_path.find("server")+7]
pack_path = server_path + 'transpiler'
sys.path.insert(0, pack_path)

from equations import PoissonTranslator, BCTranslator
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

@app.route('/submitPDE', methods=['POST'])
def getPDE():
    if request.is_json:
        json_arr = request.get_json()
        var_str = json_arr["var_str"]
        poisson_str = json_arr["poisson"].lstrip()
        dbc_str = json_arr["dbc"].lstrip()
        nbc_str = json_arr["nbc"].lstrip()
    else:
        var_str = ""
        poisson = ""
        dbc_str = ""
        nbc_str = ""

    # import pdb; pdb.set_trace()


    p = PoissonTranslator(var_str, poisson_str)
    # 暂时只支持一种bc
    if dbc_str != "":
        dbc = BCTranslator(var_str, dbc_str)
    elif nbc_str != "":
        nbc = BCTranslator(var_str, nbc_str)
    else:
        print("no bc found")
    
    return {"status": "ok"}

@app.route('/submitNN', methods=['POST'])
def runTrain():
    if request.is_json:
        json_arr = request.get_json()
        print(json_arr)
        arch = json_arr["arch"]
        lr = json_arr["lr"]
        act = json_arr["act"]
        reg = json_arr["reg"]
        init = json_arr["init"]
        batch = json_arr["batch"]
        dropout = json_arr["dropout"]
        opt = json_arr["opt"]
        loss = json_arr["loss"]
    else:
        arch = []
        lr = 0
        act = ""
        reg = ""
        init = ""
        batch = ""
        dropout = 0
        opt = ""
        loss = ""
        

    return {"status": "ok"}

    

    


if __name__ == '__main__':
    app.run()