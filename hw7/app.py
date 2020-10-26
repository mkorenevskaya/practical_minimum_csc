import os
from flask import Flask, request, abort, send_file
import json

app = Flask(__name__)


@app.route('/storage/<filename>', methods=['GET', 'PUT', 'DELETE' ])
def process(filename):
    filepath = f'storage/{filename}'
    os.makedirs('storage', exist_ok=True)
    if request.method == 'GET':
        if os.path.exists(filepath):
            return send_file(filepath), 200
        else:
            abort(404)
    elif request.method == 'PUT':
        if request.is_json:
            with open(filepath, 'w') as f:
                json.dump(request.get_json(), f)
                return '', 201
        else:
            abort(400)
    elif request.method == 'DELETE':
        if os.path.exists(filepath):
            os.remove(filepath)
        return '', 204
    else:
        print(4)

if __name__ == '__main__':
    app.run(port=8080)
