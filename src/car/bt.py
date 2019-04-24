import subprocess

import bluetooth


PASSKEY = 123456
PORT = 1


def make_connection(addr):
    # kill any "bluetooth-agent" process that is already running
    subprocess.call("kill -9 `pidof bluetooth-agent`", shell=True)

    # Start a new "bluetooth-agent" process where XXXX is the passkey
    status = subprocess.call("bluetooth-agent {} &".format(PASSKEY), shell=True)

    # Now, connect in the same way as always with PyBlueZ
    s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    s.connect((addr, PORT))
    return s
