import base64
import json
import yaml
import os 
from flask import Flask, jsonify, request
app = Flask(__name__)
app.debug=True

grain_file = '/etc/salt/grains'
USERNAME = os.environ['YMANAGE_USER']
PASSWORD = os.environ['YMANAGE_PASSWORD'] 

def is_authenticated(request):
    if 'AUTHORIZATION' not in request.headers:
        return False
    usernamepassword = base64.b64decode(request.headers['AUTHORIZATION'].split(" ")[1])
    username, password = usernamepassword.split(":")
    return USERNAME == username and PASSWORD == password

@app.route("/", methods=['GET', 'POST'])
def manage_file():
    if not is_authenticated(request): 
        return jsonify(status="not authenticated")

    if request.method == 'GET':
        file_stuff = yaml.load(file(grain_file))
        print file_stuff
        return jsonify(file_stuff)

    elif request.methods == 'POST':
        grains_data = yaml.load(file(grain_file))
        try:
            request_data = json.loads(request.data)
            new_yaml_data = request_data['grain_data']
            grains_data.update(new_yaml_data)

            with open(grains_file, 'w') as f:
                f.write(yaml.dump(grains_data))

            return jsonify(grains_data)

        except Exception as ex:
            return jsonify(status="Error")

    return jsonify(status="ok")

if __name__ == '__main__':
    app.run()
