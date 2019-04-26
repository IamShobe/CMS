import logging
import struct

import bluetooth
from bluetooth import get_l2cap_options, set_l2cap_options
from cached_property import cached_property

from implementation.core.constants import PassThrough, CType
from implementation.constants import Scope, AttributeID
from implementation.requests import GetTotalNumberOfItemsRequest, \
    GetFolderItemsRequest, SetBrowsedPlayerRequest, SetAddressedPlayerRequest, \
    PlayItemRequest, GetElementAttributesRequest, \
    GetPlayStatusRequest, GetItemAttributesRequest, NotificationRequest
from implementation.abstract_request import \
    AbstractBrowsingCommand, AbstractAVCCommand, PassThroughRequest


logger = logging.getLogger("avctp-connection")


class Connection(object):
    BROWSING_CHANNEL_PORT = 27
    CONTROL_CHANNEL_PORT = 23

    IMAGE_TARGET_HEADER_UUID = \
        "\x71\x63\xDD\x54\x4A\x7E\x11\xE2\xB4\x7C\x00\x50\xC2\x49\x00\x48"

    READ_SIZE = 1024

    def __init__(self, address,
                 control_port=CONTROL_CHANNEL_PORT,
                 browsing_port=BROWSING_CHANNEL_PORT,
                 logger=logger):
        self.address = address
        self.control_port = control_port
        self.browsing_port = browsing_port
        self.logger = logger

        self.browsing_connected = False
        self.control_connected = False

        self._control_seq = 0
        self._browsing_seq = 0

        self.unhandled_messages = []

    def log(self, message, level=logging.DEBUG, single_line=False):
        if single_line:
            message = message.replace("\r", "\\r").replace("\n", ", ")

        for line in message.split("\n"):
            self.logger.log(level, "{}".format(line))

    @property
    def control_seq(self):
        return self._control_seq

    @control_seq.setter
    def control_seq(self, value):
        self._control_seq = 0x0 if value > 0xf else value

    @property
    def browsing_seq(self):
        return self._browsing_seq

    @browsing_seq.setter
    def browsing_seq(self, value):
        self._browsing_seq = 0x0 if value > 0xf else value

    @cached_property
    def control_socket(self):
        self.log("Making control connection....", level=logging.INFO)
        socket = bluetooth.BluetoothSocket(bluetooth.L2CAP)
        socket.connect((self.address, self.control_port))
        self.control_connected = True
        return socket

    @cached_property
    def browsing_socket(self):
        self.log("Making browsing connection....", level=logging.INFO)
        socket = bluetooth.BluetoothSocket(bluetooth.L2CAP)
        settings = get_l2cap_options(socket)
        settings[3] = 3
        set_l2cap_options(socket, settings)
        socket.connect((self.address, self.browsing_port))
        self.browsing_connected = True
        return socket

    def send_control_message(self, message):
        message.seq = self.control_seq
        self.control_seq += 1
        self.log("Sending control message {} with sequence {}".format(
            message, message.seq))
        self.control_socket.send(message.pack())

    def send_browsing_message(self, message):
        message.seq = self.browsing_seq
        self.browsing_seq += 1
        self.log("Sending browsing message {} with sequence {}".format(
            message, message.seq))
        self.browsing_socket.send(message.pack())

    def _get_msg(self):
        self.log("Waiting for response from socket")
        content = self.control_socket.recv(self.READ_SIZE)

        # force all received messages to be set to receive
        # I encountered that EVENT pdu's are returned as requester.
        content = struct.pack("B", (ord(content[0]) | 2)) + content[1:]
        msg = AbstractAVCCommand.unpack(content)
        self.log("New message received: {}, seq: {}".format(msg, msg.seq))
        if msg.packet.ctype == CType.NOTIFY:
            self.log("New event received! {}".format(msg.event),
                     level=logging.WARNING)
            self.unhandled_messages.append(msg)
            self.log("Adding to unhandled messages..", level=logging.WARNING)
            return None

        return msg

    def read_control_channel(self):
        msg = self._get_msg()
        while msg is None:
            msg = self._get_msg()
        self.log("Matched control message!".format(msg))
        return msg

    def read_browsing_channel(self):
        content = self.browsing_socket.recv(self.READ_SIZE)
        msg = AbstractBrowsingCommand.unpack(content)
        self.log("Matched browsing message: {}".format(msg))
        return msg

    def connect(self):
        self.control_socket
        self.browsing_socket

    def close(self):
        if self.browsing_connected:
            self.browsing_socket.close()

        if self.control_connected:
            self.control_socket.close()

    def get_total_number_of_items(self, scope):
        message = GetTotalNumberOfItemsRequest(scope=scope)

        self.send_browsing_message(message)
        return self.read_browsing_channel()

    def set_browsed_player(self, player_id):
        message = SetBrowsedPlayerRequest(player_id=player_id)

        self.send_browsing_message(message)
        return self.read_browsing_channel()

    def set_addressed_player(self, player_id):
        message = SetAddressedPlayerRequest(player_id=player_id)

        self.send_control_message(message)
        return self.read_control_channel()

    def play_first_item(self):
        message = PlayItemRequest(scope=Scope.NOW_PLAYING,
                                  uid=1,
                                  uid_counter=0)

        self.send_control_message(message)
        return self.read_control_channel()

    def list_media_players(self):
        message = GetFolderItemsRequest(scope=Scope.MEDIA_PLAYER,
                                        start_item=0,
                                        end_item=1,
                                        attributes_count=0)

        self.send_browsing_message(message)
        return self.read_browsing_channel()

    def list_played_items(self):
        message = GetFolderItemsRequest(scope=Scope.NOW_PLAYING,
                                        start_item=0,
                                        end_item=2,
                                        attributes_count=0)
        self.send_browsing_message(message)
        return self.read_browsing_channel()

    def get_track_info(self):
        message = GetElementAttributesRequest()

        self.send_control_message(message)
        return self.read_control_channel()

    def get_current_track_image(self):
        message = GetElementAttributesRequest(
            attributes=[AttributeID.DEFAULT_COVER_ART])

        self.send_control_message(message)
        return self.read_control_channel()

    def get_track_image_of(self, uid):
        message = GetItemAttributesRequest(
            scope=Scope.NOW_PLAYING,
            uid=uid,
            uid_counter=0,
            attributes=[AttributeID.DEFAULT_COVER_ART])

        self.send_browsing_message(message)
        return self.read_browsing_channel()

    def register_event(self, event_id):
        message = NotificationRequest(event_id=event_id)

        self.send_control_message(message)
        return self.read_control_channel()

    def get_play_status(self):
        message = GetPlayStatusRequest()

        self.send_control_message(message)
        return self.read_control_channel()

    def play(self):
        message = PassThroughRequest(operation_id=PassThrough.PLAY)

        self.send_control_message(message)
        return self.read_control_channel()

    def pause(self):
        message = PassThroughRequest(operation_id=PassThrough.PAUSE)

        self.send_control_message(message)
        return self.read_control_channel()

    def stop(self):
        message = PassThroughRequest(operation_id=PassThrough.STOP)

        self.send_control_message(message)
        return self.read_control_channel()

    def next_song(self):
        message = PassThroughRequest(operation_id=PassThrough.FORWARD)

        self.send_control_message(message)
        return self.read_control_channel()

    def prev_song(self):
        message = PassThroughRequest(operation_id=PassThrough.BACKWARD)

        self.send_control_message(message)
        return self.read_control_channel()

    def vol_up(self):
        message = PassThroughRequest(operation_id=PassThrough.VOL_UP)

        self.send_control_message(message)
        return self.read_control_channel()

    def vol_down(self):
        message = PassThroughRequest(operation_id=PassThrough.VOL_DOWN)

        self.send_control_message(message)
        return self.read_control_channel()

    def mute(self):
        message = PassThroughRequest(operation_id=PassThrough.MUTE)

        self.send_control_message(message)
        return self.read_control_channel()

    def skip(self):
        message = PassThroughRequest(operation_id=PassThrough.SKIP)

        self.send_control_message(message)
        return self.read_control_channel()
    # def list_folder(self):
    #     message = GetTotalNumberOfItemsRequest(scope=Scope.MEDIA_PLAYER)
    #     message.seq = self.browsing_seq
    #     self.browsing_seq += 1
    #
    #     self.send_browsing_message(message)
    #     return self.read_browsing_channel()
