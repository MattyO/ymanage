import json
import yaml
import os 
from flask import Flask, jsonify
app = Flask(__name__)

grain_file = '/etc/salt/grains'
username = os.environ['YMANAGE_USER']
password = os.environ['YMANAGE_PASSWORD'] 

@app.route("/", method=['GET', 'POST'])
def manage_file():
    if request.method == 'GET':
        return jsonify(yaml.load(file(grain_file)))

    elif request.method == 'POST':
        grains_data = yaml.load(file(grain_file))
        try:
            request_data = json.loads(request.data)
            if request_data['username'] != username and request_data['password'] != password:
                return jsonfigy(status="not authorized")

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
