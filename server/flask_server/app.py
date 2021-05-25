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

import matplotlib
matplotlib.use('agg')

import json

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

class Backbone:
    def __init__(self):
        super().__init__()
    
    @staticmethod
    def boundary(_, on_boundary):
        return on_boundary

    def get_geo(self, xde_obj):
        self.geom = xde_obj

    def get_equations(self, poisson, bc, bc_type):
        if bc_type == "d": #dirichlet
            self.bc = dde.DirichletBC(self.geom, bc, self.boundary)
        else: #neumann
            self.bc = dde.NeumannBC(self.geom, bc, self.boundary)
        self.pde = poisson

    def get_net(self, params_list):
        data = dde.data.PDE(
            self.geom, 
            self.pde, 
            self.bc, 
            num_domain=params_list[9], 
            num_boundary=params_list[10], 
            train_distribution=params_list[12],
            num_test=params_list[11])
        net = dde.maps.FNN(
            [2] + params_list[0] + [1],
            activation = params_list[2],
            kernel_initializer = params_list[4],
            regularization=params_list[3],
            dropout_rate=params_list[6],
            batch_normalization=params_list[5])
        self.model = dde.Model(data, net)
        self.model.compile(
            optimizer = params_list[7],
            lr = params_list[1],
            loss = params_list[8]
        )

    def run(self):
        losshistory, train_state = self.model.train(epochs=5000)
        dde.saveplot(losshistory, train_state, issave=False, isplot=True)
    

backbone = Backbone()



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
    # build xde model
    geom_obj_id = xde_obj_dicts["target_id"]
    backbone.get_geo(xde_obj_dicts[geom_obj_id].xde_geom)
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
        bc = BCTranslator(var_str, dbc_str)
        bc_type = "d"
    elif nbc_str != "":
        bc = BCTranslator(var_str, nbc_str)
        bc_type = "n"
    else:
        bc = None
        bc_type = None
        print("no bc found")
    
    backbone.get_equations(p.get(), bc.get(), bc_type)
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
        n_domain = json_arr["n_domain"]
        n_bc = json_arr["n_bc"]
        n_test = json_arr["n_test"]
        dist = json_arr["dist"]
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
        n_domain = 0
        n_bc = 0
        n_test = 0
        dist = ""

    # import pdb; pdb.set_trace()
    param_list = [arch, lr, act, reg, init, batch, dropout, opt, loss, n_domain, n_bc, n_test, dist]
    backbone.get_net(param_list)
    backbone.run()
        

    return {"status": "ok"}

    

    


if __name__ == '__main__':
    app.run()