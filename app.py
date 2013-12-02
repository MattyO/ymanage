import json
import yaml
from flask import Flask, jsonify
app = Flask(__name__)

grain_file = '/etc/salt/grains'

@app.route("/", method=['GET', 'POST'])
def manage_file():
    if request.method == 'GET':
        return jsonify(yaml.load(file(grain_file)))

    elif request.method == 'POST':
        grains_data = yaml.load(file(grain_file))
        try
            new_yaml_data = json.loads(request.data)
            grains_data.update(new_yaml_data)

            with open(grains_file, 'w') as f:
                f.write(yaml.dump(grains_data))

            return jsonify(grains_data)

        except Exception ex:
            return jsonify(status="Error")

    return jsonify(status="ok")


