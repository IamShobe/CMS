import eventlet
eventlet.monkey_patch()

import requests

from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, logger=True, engineio_logger=True)

connection = None
actions = []


@app.route('/api/bluetooth/devices/scan/')
def scan_devices():
    data = requests.get("http://localhost:8090/api/devices/scan")
    response = app.response_class(
        response=data,
        status=200,
        mimetype='application/json'
    )

    return response


@app.route('/api/bluetooth/devices/')
def get_devices():
    data = requests.get("http://localhost:8090/api/devices")
    response = app.response_class(
        response=data,
        status=200,
        mimetype='application/json'
    )

    return response


@app.route('/api/bluetooth/pair/', methods=["POST"])
def connect_device():
    data = requests.post("http://localhost:8090/api/pair",
                         json=request.json)
    response = app.response_class(
        response=data,
        status=data.status_code,
        mimetype='application/json'
    )

    return response


@socketio.on('connect')
def test_message():
    emit('event', {'data': 'got it!'})


@socketio.on('pair', namespace="/pair")
def test_message(data):
    print "pair request received!"
    print data
    socketio.emit('pairing_request', data, namespace="/client")


@socketio.on('pair_response', namespace="/client")
def new_pair(msg):
    socketio.emit("pair_response", msg, namespace="/pair")


# def bg_emit():
#     socketio.emit('bg_emit', dict(foo='bar'))
#
#
# def listen():
#     while True:
#         bg_emit()
#         # accept_connections()
#         eventlet.sleep(5)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def main(path):
    return render_template('index.html')


if __name__ == '__main__':
    # eventlet.spawn(listen)
    socketio.run(app, host="0.0.0.0", port=8080, debug=True)

    print "App exited!"
