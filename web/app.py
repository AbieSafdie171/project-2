"""
Abie Safdie's Flask API.
"""

import os
import configparser
from flask import Flask, abort, send_from_directory

app = Flask(__name__)


def parse_config(config_paths):
    config_path = None
    for f in config_paths:
        if os.path.isfile(f):
            config_path = f
            break

    if config_path is None:
        raise RuntimeError("Configuration file not found!")

    config = configparser.ConfigParser()
    config.read(config_path)
    return config


config = parse_config(["credentials.ini", "default.ini"])
PORT_NUM = config["SERVER"]["PORT"]
DEBUG_MODE = config["SERVER"]["DEBUG"]


@app.route("/<string:request>")
def hello(request):
    if "~" in request or ".." in request:
        abort(403)
    if len(request) < 1:
        abort(403)
    try:
        f = open(f'pages/{request}', 'r')
        return send_from_directory('pages/', f'{request}'), 200

    except:
        abort(404)
@app.errorhandler(404)
def notFound(e):
    return send_from_directory('pages/', '404.html'), 404

@app.errorhandler(403)
def forbidden(e):
    return send_from_directory('pages/', '403.html'), 403


if __name__ == "__main__":
    app.run(debug=DEBUG_MODE, host='0.0.0.0', port=PORT_NUM)
