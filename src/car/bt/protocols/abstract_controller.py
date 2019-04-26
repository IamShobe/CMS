import logging


class ProtocolController(object):
    SERVICE_CLASS = NotImplemented

    def __init__(self, address, logger=logging.getLogger("Bluetooth")):
        self.address = address
        self.logger = logger

        self.connection = None

    def log(self, message, context="General", level=logging.DEBUG,
            single_line=False, logger=None):
        if single_line:
            message = message.replace("\r", "\\r").replace("\n", ", ")

        for line in message.split("\n"):
            if logger is None:
                logger = self.logger

            logger.log(level, "{} - {} - {}".format(
                self.__class__.__name__, context, line))

    def connect(self, port):
        self.log("Making connection to: {}".format(self.address))
        self.connection = self._connect(port)
        self.log("Connected!")

    def _connect(self, port):
        pass

    def _close(self):
        pass

    def close(self):
        self.log("Closing connection..")
        if self.connection:
            self._close()
            self.connection = None
        self.log("Closed!")

    def __del__(self):
        if self.connection:
            self.close()
