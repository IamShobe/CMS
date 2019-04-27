import json

from flask import Flask, request

from car.bt.controller import BTController, logger
from logger.logger import paint_logger

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
bt_controller = BTController()
paint_logger(logger)


@app.route('/api/devices/scan/')
def scan_devices():
    devices = bt_controller.probe_devices()
    response = app.response_class(
        response=json.dumps(devices),
        status=200,
        mimetype='application/json'
    )

    return response


@app.route('/api/devices/')
def get_cached_devices():
    devices = bt_controller.cached_addresses
    response = app.response_class(
        response=json.dumps(devices),
        status=200,
        mimetype='application/json'
    )

    return response


@app.route('/api/pair', methods=["POST"])
def connect_device():
    data = request.get_json(force=True)
    to_connect = data['address']
    device = bt_controller.get_client(to_connect)
    device.pair()
    # device.close()
    response = app.response_class(
        response=json.dumps({}),
        status=200,
        mimetype='application/json'
    )

    return response


if __name__ == '__main__':
    app.run(port=8090)
