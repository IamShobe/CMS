import struct

import bluetooth
from bluetooth import get_l2cap_options, set_l2cap_options
from cached_property import cached_property

from car.bt.protocols.avctp.implementation.core.constants import PassThrough
from implementation.constants import Scope
from implementation.requests import GetTotalNumberOfItemsRequest, \
    GetFolderItemsRequest, SetBrowsedPlayerRequest, SetAddressedPlayerRequest, \
    PlayItemRequest, GetElementAttributesRequest, GetPlayStatusResponse, \
    GetPlayStatusRequest
from implementation.abstract_request import \
    AbstractBrowsingCommand, AbstractAVCCommand, PassThroughRequest


class Connection(object):
    BROWSING_CHANNEL_PORT = 27
    CONTROL_CHANNEL_PORT = 23

    READ_SIZE = 1024

    def __init__(self, address,
                 control_port=CONTROL_CHANNEL_PORT,
                 browsing_port=BROWSING_CHANNEL_PORT):
        self.address = address
        self.control_port = control_port
        self.browsing_port = browsing_port

        self.browsing_connected = False
        self.control_connected = False

        self._control_seq = 1
        self._browsing_seq = 1

        self.unhandled_messages = []

    @property
    def control_seq(self):
        return self._control_seq

    @control_seq.setter
    def control_seq(self, value):
        self._control_seq = 0x1 if value > 0xf else value

    @property
    def browsing_seq(self):
        return self._browsing_seq

    @browsing_seq.setter
    def browsing_seq(self, value):
        self._browsing_seq = 0x1 if value > 0xf else value

    @cached_property
    def control_socket(self):
        socket = bluetooth.BluetoothSocket(bluetooth.L2CAP)
        socket.connect((self.address, self.control_port))
        self.control_connected = True
        return socket

    @cached_property
    def browsing_socket(self):
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
        self.control_socket.send(message.pack())

    def send_browsing_message(self, message):
        message.seq = self.browsing_seq
        self.browsing_seq += 1
        self.browsing_socket.send(message.pack())

    def _get_msg(self, msg_seq):
        content = self.control_socket.recv(self.READ_SIZE)

        # force all received messages to be set to receive
        # I encountered that EVENT pdu's are returned as requester.
        content = struct.pack("B", (ord(content[0]) | 2)) + content[1:]
        msg = AbstractAVCCommand.unpack(content)

        if msg.seq != msg_seq:
            self.unhandled_messages.append(msg)
            return None

        return msg

    def read_control_channel(self, msg_seq):
        msg = self._get_msg(msg_seq)
        while msg is None:
            msg = self._get_msg(msg_seq)

        return msg

    def read_browsing_channel(self):
        content = self.browsing_socket.recv(self.READ_SIZE)
        return AbstractBrowsingCommand.unpack(content)

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
        return self.read_control_channel(message.seq)

    def play_first_item(self):
        message = PlayItemRequest(scope=Scope.NOW_PLAYING,
                                  uid=1,
                                  uid_counter=1)

        self.send_control_message(message)
        return self.read_control_channel(message.seq)

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
        return self.read_control_channel(message.seq)

    def get_play_status(self):
        message = GetPlayStatusRequest()

        self.send_control_message(message)
        return self.read_control_channel(message.seq)

    def play(self):
        message = PassThroughRequest(operation_id=PassThrough.PLAY)

        self.send_control_message(message)
        return self.read_control_channel(message.seq)

    def pause(self):
        message = PassThroughRequest(operation_id=PassThrough.PAUSE)

        self.send_control_message(message)
        return self.read_control_channel(message.seq)

    def stop(self):
        message = PassThroughRequest(operation_id=PassThrough.STOP)

        self.send_control_message(message)
        return self.read_control_channel(message.seq)

    def next_song(self):
        message = PassThroughRequest(operation_id=PassThrough.FORWARD)

        self.send_control_message(message)
        return self.read_control_channel(message.seq)

    def prev_song(self):
        message = PassThroughRequest(operation_id=PassThrough.BACKWARD)

        self.send_control_message(message)
        return self.read_control_channel(message.seq)

    def vol_up(self):
        message = PassThroughRequest(operation_id=PassThrough.VOL_UP)

        self.send_control_message(message)
        return self.read_control_channel(message.seq)

    def vol_down(self):
        message = PassThroughRequest(operation_id=PassThrough.VOL_DOWN)

        self.send_control_message(message)
        return self.read_control_channel(message.seq)

    def mute(self):
        message = PassThroughRequest(operation_id=PassThrough.MUTE)

        self.send_control_message(message)
        return self.read_control_channel(message.seq)

    def skip(self):
        message = PassThroughRequest(operation_id=PassThrough.SKIP)

        self.send_control_message(message)
        return self.read_control_channel(message.seq)
    # def list_folder(self):
    #     message = GetTotalNumberOfItemsRequest(scope=Scope.MEDIA_PLAYER)
    #     message.seq = self.browsing_seq
    #     self.browsing_seq += 1
    #
    #     self.send_browsing_message(message)
    #     return self.read_browsing_channel()
