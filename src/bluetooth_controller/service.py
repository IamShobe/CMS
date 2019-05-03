import json

from flask import Flask, request

from logger.logger import paint_logger

from .controller import BTController, logger


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


@app.route('/api/devices/available/')
@app.route('/api/devices/')
def get_available_devices():
    devices = bt_controller.available_devices
    response = app.response_class(
        response=json.dumps(devices),
        status=200,
        mimetype='application/json'
    )

    return response


@app.route('/api/devices/pairable/')
def get_pairable_devices():
    devices = bt_controller.devices_to_pair
    response = app.response_class(
        response=json.dumps(devices),
        status=200,
        mimetype='application/json'
    )

    return response


@app.route('/api/devices/paired/')
def get_paired_devices():
    devices = bt_controller.paired_devices
    response = app.response_class(
        response=json.dumps(devices),
        status=200,
        mimetype='application/json'
    )

    return response


@app.route('/api/devices/connected/')
def get_connected_devices():
    devices = bt_controller.connected_devices
    response = app.response_class(
        response=json.dumps(devices),
        status=200,
        mimetype='application/json'
    )

    return response


@app.route('/api/devices/<string:address>/alive/', methods=["GET"])
def device_is_alive(address):
    device = bt_controller.get_client(address)

    response = app.response_class(
        response=json.dumps({
            "alive": device.is_alive()
        }),
        status=200,
        mimetype='application/json'
    )

    return response


@app.route('/api/devices/<string:address>/services/', methods=["GET"])
def services_device(address):
    device = bt_controller.get_client(address)

    response = app.response_class(
        response=json.dumps({
            "services": [service.to_dict()
                         for service in device.services.values()]
        }),
        status=200,
        mimetype='application/json'
    )

    return response


@app.route('/api/devices/<string:address>/pair/', methods=["POST"])
def pair_device(address):
    device = bt_controller.get_client(address)
    device.pair_and_trust()

    response = app.response_class(
        response=json.dumps({}),
        status=200,
        mimetype='application/json'
    )

    return response


@app.route('/api/devices/<string:address>/connect/', methods=["POST"])
def connect_device(address):
    device = bt_controller.get_client(address)
    device.connect()

    response = app.response_class(
        response=json.dumps({}),
        status=200,
        mimetype='application/json'
    )

    return response


@app.route('/api/devices/<string:address>/disconnect/', methods=["POST"])
def disconnect_device(address):
    device = bt_controller.get_client(address)
    device.close()

    response = app.response_class(
        response=json.dumps({}),
        status=200,
        mimetype='application/json'
    )

    return response


@app.route('/api/devices/<string:address>/remove/', methods=["POST"])
def remove_device(address):
    device = bt_controller.get_client(address)
    device.remove()

    response = app.response_class(
        response=json.dumps({}),
        status=200,
        mimetype='application/json'
    )

    return response


@app.route('/api/devices/<string:address>/phonebook/', methods=["GET"])
def get_device_phonebook(address):
    device = bt_controller.get_client(address)

    response = app.response_class(
        response=json.dumps([contact.to_dict()
                             for contact in device.pbap.get_phonebook()]),
        status=200,
        mimetype='application/json'
    )

    return response


if __name__ == '__main__':
    app.run(port=8090)
