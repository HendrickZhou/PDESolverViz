from flask import Flask
app = Flask("nn")

# @app.route('/nn_arch', method=['POST'])
@app.route('/')
def get_nn_arch():
    return "Hello"
