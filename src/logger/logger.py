from __future__ import  unicode_literals

import os
import sys
import logging

from logging.handlers import RotatingFileHandler
# from utils.constants import BASE_DIR, PROJECT_NAME

MAX_LOG_SIZE = 10000000  # 10 MB

FORMAT = '%(asctime)s %(levelname)s %(name)s: %(message)s'

# file_handler_g = RotatingFileHandler(
#     filename=os.path.join(BASE_DIR, "logs/{}.log".format(PROJECT_NAME)),
#     maxBytes=MAX_LOG_SIZE,
#     backupCount=5
# )
# file_handler_g.formatter = formatter
formatter = logging.Formatter(fmt=FORMAT)


class ColorFormatter(logging.Formatter):
    """ A log formatter with color injection. """

    def __init__(self, fmt=FORMAT,
                 datefmt='%H:%M:%S', reset='\x1b[0m'):
        """ Better format defaults. Reset code can be overridden if
        necessary."""
        logging.Formatter.__init__(self, fmt=fmt, datefmt=datefmt)
        self.reset = reset

    def format(self, record):
        """ Inject color codes & color resets into log record messages. """
        message = logging.Formatter.format(self, record)

        try:
            color = logging._levelColors[record.levelno]
            message = color + message + self.reset
        except:
            pass

        return message


class ColorStreamHandler(logging.StreamHandler):
    """ StreamHandler with better defaults. """

    def __init__(self, level=logging.DEBUG, stream=sys.stdout,
                 formatter=ColorFormatter()):
        """ Sets the handler level to DEBUG (rather than ERROR) by default. Uses
        stderr instead of stdout. Binds the ColorFormatter if another Formatter
        hasn't been provided. """
        logging.StreamHandler.__init__(self, stream=stream)

        if formatter is not None:
            self.setFormatter(formatter)


def paint_logger(logger):
    colormap = {50: '\x1b[1;31m',
                40: '\x1b[31m',
                30: '\x1b[33m',
                20: '\x1b[32m',
                10: '\x1b[35m'}
    handler = ColorStreamHandler()
    logging._levelColors = colormap
    logger.addHandler(handler)


class ColorLogger(logging.Logger):
    """ A ColorLogger class with default colormap and convenience methods. """

    def __init__(self, name, level=logging.DEBUG, propagate=False, handlers=None, colormap=None):
        # If logging._levelColors is not defined, define it.
        if colormap is None:
            colormap = {50: '\x1b[1;31m',
                        40: '\x1b[31m',
                        30: '\x1b[33m',
                        20: '\x1b[32m',
                        10: '\x1b[35m'}

        # file_handler = RotatingFileHandler(
        #     filename=os.path.join(BASE_DIR, "logs/{}_{}.log".format(PROJECT_NAME, name)),
        #     maxBytes=MAX_LOG_SIZE,
        #     backupCount=5
        # )
        # file_handler.formatter = formatter

        if handlers is None:
            handlers = [ColorStreamHandler()]
        try:
            colors = logging._levelColors
        except:
            colors = logging._levelColors = colormap

        # Set the logger's level.
        logging.Logger.__init__(self, name, level=level)

        # Disable propagation.
        self.propagate = propagate

        # Add any default handlers. By default this is the ColorHandler.
        for handler in handlers:
            self.addHandler(handler)

    @staticmethod
    def _getLevelNumbers():
        """ Returns the integer keys from the levelNames dictionary. """
        return [ik for ik in logging._levelNames.keys() if type(ik) is int]

    @staticmethod
    def _getLevelNames():
        """ Returns the string keys from the levelNames dictionary. """
        return [sk for sk in logging._levelNames.keys() if type(sk) is str]

    @staticmethod
    def addLevel(levelno, name, color):
        """ Adds a custom logging level with color. """
        logging._levelNames[levelno] = name
        logging._levelColors[levelno] = color


def get_logger(name, mode=logging.DEBUG):
    """Fetch new logger and set it's name and mode.

    Args:
        name (unicode): a name of the logger.
        mode (number): either logging.DEBUG, logging.WARNING, logging.CRITICAL, logging.INFO etc.

    Returns:
        logging.Logger. a requested logger.
    """
    logger = ColorLogger(name, mode)
    return logger
