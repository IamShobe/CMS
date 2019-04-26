import logging

import bluetooth

from car.bt.protocols.abstract_controller import ProtocolController


hfp_logger = logging.getLogger("hfp-protocol")


class HFPController(ProtocolController):
    SERVICE_CLASS = "111F"

    def write_message(self, msg, context="General"):
        self.log("Writing: {}".format(msg), context=context, logger=hfp_logger)
        self.connection.send("{}\r".format(msg))

    def read_until_cr(self, max_c=100):
        buffer = ""
        current_c = 0
        try:
            while current_c < max_c:
                byte = self.connection.recv(1)
                buffer += byte
                current_c += 1
                if byte in ["\n", "\r"]:
                    if buffer.strip() != "":
                        break

        except:
            pass

        return buffer.strip()

    def read_until_ok(self, max_ln=8):
        buffer = ""
        for _ in xrange(max_ln):
            current = self.read_until_cr()
            if current.startswith("+") or current in ["OK", "ERROR"]:
                buffer += "\n"

            buffer += current
            if current == "OK":
                break

            elif current == "ERROR":
                current = self.read_until_cr()
                buffer += current
                break

        return buffer.strip()

    def execute_command(self, command, context="General"):
        self.write_message(command, context=context)
        self.log("Receiving: " + self.read_until_ok(), context=context,
                 single_line=True, logger=hfp_logger)

    def _connect(self, port):
        s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        s.connect((self.address, port))
        self.connection = s

        self.execute_command("AT+BRSF=3943", context="Connection")
        self.execute_command("AT+CIND=?", context="Connection")
        self.execute_command("AT+CIND?", context="Connection")
        self.execute_command("AT+CMER=3,0,0,1", context="Connection")
        self.execute_command("AT+CMEE=1", context="Connection")
        self.execute_command("AT+BIA=1,1,1,1,1,1,1", context="Connection")
        self.execute_command("AT+CLIP=1", context="Connection")
        self.execute_command("AT+CCWA=1", context="Connection")
        self.execute_command("AT+CHLD=?", context="Connection")
        self.execute_command("AT+BIND=1,2", context="Connection")
        self.execute_command("AT+BIND?", context="Connection")
        self.execute_command("AT+BIND?", context="Connection")
        self.execute_command("AT+CLCC", context="Connection")

        return s

    def _close(self):
        self.connection.close()
