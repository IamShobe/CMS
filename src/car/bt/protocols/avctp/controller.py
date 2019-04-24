import struct

import bluetooth
from bluetooth import set_l2cap_options, get_l2cap_options

from car.bt.protocols.abstract_controller import ProtocolController
from car.bt.protocols.avctp.avctp import parse_avrcp, sendcapabilityreq, nextseq

MAX_PACKET_MTU = 23  # bytes
AVRCP_CTYPE_CONTROL = 0
AVRCP_CTYPE_STATUS = 1
AVRCP_CTYPE_SPECIFIC_INQUIRY = 2
AVRCP_CTYPE_NOTIFY = 3
AVRCP_CTYPE_GENERAL_INQUIRY = 4
AVRCP_CTYPE_RESPONSE_NOT_IMPLEMENTED = 8
AVRCP_CTYPE_RESPONSE_ACCEPTED = 9
AVRCP_CTYPE_RESPONSE_REJECTED = 0xA
AVRCP_CTYPE_RESPONSE_IN_TRANSITION = 0xb
AVRCP_CTYPE_RESPONSE_IMPLEMENTED = 0xc
AVRCP_CTYPE_RESPONSE_CHANGED = 0xd
AVRCP_CTYPE_RESPONSE_RESERVED = 0xe
AVRCP_CTYPE_RESPONSE_INTERIM = 0xf
AVRCP_HEADER = "\x48\x00\x00\x19\x58"


PID = "\x11\x0E"


L2CAP_SETTINGS = [512, 672, 65535, 3, 0, 3, 63]


class AVCTPController(ProtocolController):
    SERVICE_CLASS = "110E"

    FULL_PACKET = 0b00
    START_PACKET = 0b10
    END_PACKET = 0b01
    CONTINUE_PACKET = 0b11

    RESERVED = 0b000000

    def send_avctp_msg(self, *params):
        seq = nextseq()
        # packet = struct.pack(">B", (seq << 4) | (0b00 << 2) | (0b0 << 1) | 0b0)
        # packet += PID
        packet = ""
        for param in params:
            packet += struct.pack(">" + ("B" * len(param)), *[ord(c) for c in param])

        s = ""
        print "writing:"
        for b in packet:
            s += ("%02x" % ord(b)) + " "
        print s

        self.connection.send(packet)

    def send_msg(self, pdu, data="", packet_type=FULL_PACKET, ctype=AVRCP_CTYPE_STATUS):
        seq = nextseq()
        packet = struct.pack(">B", (seq << 4) | (0b00 << 2) | (0b0 << 1) | 0b0)
        packet += PID

        packet += struct.pack(">B", ctype)
        packet += AVRCP_HEADER
        packet += struct.pack(">BB", pdu, self.RESERVED << 2 | packet_type)
        packet += struct.pack(">H", len(data))
        packet += data
        s = ""
        print "writing:"
        for b in packet:
            s += ("%02x" % ord(b)) + " "
        print s

        self.connection.send(packet)

    def send_browse_msg(self, pdu, data):
        seq = nextseq()
        packet = struct.pack(">B", (seq << 4) | (0b00 << 2) | (0b0 << 1) | 0b0)
        packet += PID

        packet += struct.pack(">B", pdu)
        packet += struct.pack(">H", len(data))
        packet += data
        s = ""
        print "browsing writing:"
        for b in packet:
            s += ("%02x" % ord(b)) + " "
        print s

        self.browsing.send(packet)

    def read_response(self):
        print "response:"
        content = self.connection.recv(1024)
        s = ""
        for b in content:
            s += ("%02x" % ord(b)) + " "
        print s
        parse_avrcp(content)

    def read_browsing_response(self):
        print "browsing response:"
        content = self.browsing.recv(1024)
        s = ""
        for b in content:
            s += ("%02x" % ord(b)) + " "
        print s
        parse_avrcp(content)

    def _connect(self, port):
        s = bluetooth.BluetoothSocket(bluetooth.L2CAP)
        s.connect((self.address, port))

        browsing = bluetooth.BluetoothSocket(bluetooth.L2CAP)
        settings = get_l2cap_options(browsing)
        settings[3] = 3
        set_l2cap_options(browsing, settings)
        browsing.connect((self.address, 27))
        self.connection = s
        self.browsing = browsing

        return s

    def _close(self):
        self.browsing.close()
        self.connection.close()


if __name__ == '__main__':
    address = "C0:EE:FB:D5:FC:A2"
    port = 23
    conn = AVCTPController(address)
    conn.connect(port)

    conn.send_browse_msg(0x71, data="\x00" + "\x00\x00\x00\x00" + "\x00\x00\x00\x03" + "\x00")
    conn.read_browsing_response()

    conn.send_msg(0x60, ctype=AVRCP_CTYPE_CONTROL,
                  data="\x00\x03")
    conn.read_response()
    conn.read_response()

    conn.send_browse_msg(0x71,
                         data="\x03" + "\x00\x00\x00\x00" + "\x00\x00\x00\x03" + "\x01" + "\x00\x00\x00\x01")
    conn.read_browsing_response()


    conn.send_msg(0x74, data="\x03" + "\x00\x00\x00\x00\x00\x00\x00\x02" + "\x00\x01",
               ctype=AVRCP_CTYPE_CONTROL)
    conn.read_response()

    # conn.send_browse_msg()
    # conn.send_avctp_msg("\xc0\xee\xfb\xd5\xfc\xa2", PID)


    # sendcapabilityreq(conn.connection)
    # conn.read_response()
    # content = conn.connection.recv(1024)
    # s = ""
    # for b in content:
    #     s += ("%02x" % ord(b)) + " "
    # print s
    # parse_avrcp(content)
    import ipdb; ipdb.set_trace()
