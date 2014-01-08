import base64
import json
import yaml
import os 
from flask import Flask, jsonify, request
app = Flask(__name__)
app.debug=True

grain_file = '/etc/salt/grains'
#grain_file = 'grains'
USERNAME = os.environ['YMANAGE_USER']
PASSWORD = os.environ['YMANAGE_PASSWORD'] 

def is_authenticated(request):
    if 'AUTHORIZATION' not in request.headers:
        return False
    usernamepassword = base64.b64decode(request.headers['AUTHORIZATION'].split(" ")[1])
    username, password = usernamepassword.split(":")
    return USERNAME == username and PASSWORD == password

@app.route("/ping", methods=['GET'])
def ping(request):
    if not is_authenticated(request): 
        return jsonify(status="not authenticated")

    return jsonify({"status":"ok"})

@app.route("/", methods=['GET', 'PUT'])
def manage_file(request):
    if not is_authenticated(request): 
        return jsonify(status="not authenticated")

    if request.method == 'GET':
        file_stuff = yaml.load(file(grain_file))
        print file_stuff
        return jsonify(file_stuff)

    elif request.method == 'PUT':
        try:
            grains_data = yaml.load(file(grain_file))
            request_data = json.loads(request.data)
            grains_data.update(request_data)

            yaml.safe_dump(grains_data,file(grain_file, 'w'), default_flow_style=False, indent=2)
            

            return jsonify(grains_data)

        except Exception as ex:
            return jsonify(status="Error", message = ex.message)

    return jsonify(status="ok")

if __name__ == '__main__':
    app.run()
