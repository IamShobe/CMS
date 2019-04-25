from constants import PDU, CType, PassThrough
from abstract_packet import Packet
from fields import Field, UnknownSizeField


class AVRTPPacket(Packet):
    FIELDS = [
        Field("seq", bits=4),
        Field("avrtp_type", bits=2, default=0),
        Field("cr", bits=1),
        Field("ipid", bits=1, default=0),
        Field("pid", bits=16, default="\x11\x0E")
    ]

    def is_valid(self):
        return self.ipid == 0

    @property
    def validity(self):
        return "Valid" if self.is_valid else "InValid"

    @property
    def msg_type(self):
        return "Request" if not self.cr else "Response"

    def __repr__(self):
        return "{}(label={}, cr={}, validity={})".format(
            self.__class__.__name__, self.seq, self.msg_type, self.validity)


class AVCPacket(Packet):
    BASE_PACKET = AVRTPPacket
    FIELDS = [
        Field("header", bits=4, default=0),
        Field("ctype", bits=4, default=0, type=CType),
        Field("subunit_type", bits=6, default=0x9),  # panel subunit
        Field("subunit_id", bits=2, default=0, type=int),
        Field("op_code", bits=8, default="\x7C", type=int)
    ]

    def __repr__(self):
        return "{}(op_code={}, ctype={})".format(self.__class__.__name__,
                                                 self.op_code,
                                                 self.ctype)


class PassThroughPacket(Packet):
    BASE_PACKET = AVRTPPacket
    FIELDS = [
        Field("header", bits=4, default=0),
        Field("ctype", bits=4, default=0, type=CType),
        Field("subunit_type", bits=6, default=0x9),  # panel subunit
        Field("subunit_id", bits=2, default=0, type=int),
        Field("op_code", bits=8, default="\x7C", type=int),
        Field("state_flag", bits=1, default=0, type=int),
        Field("operation_id", bits=7, type=PassThrough),
        Field("parameters_length", bits=8, default=0, type=int),
        UnknownSizeField("parameters", linked_length_field="parameters_length")
    ]

    def __repr__(self):
        return "{}(operation_id={}, ctype={})".format(self.__class__.__name__,
                                                      self.operation_id,
                                                      self.ctype)


class ControlPacket(Packet):
    BASE_PACKET = AVRTPPacket
    FIELDS = [
        Field("header", bits=4, default=0),
        Field("ctype", bits=4, default=0, type=CType),
        Field("subunit_type", bits=6, default=18),
        Field("subunit_id", bits=2, default=0, type=int),
        Field("op_code", bits=8, default="\x00", type=int),
        Field("company_id", bits=24, default="\x00\x19\x58"),
        Field("pdu_id", bits=8, type=PDU),
        Field("reserved", bits=6, default=0),
        Field("type", bits=2, default=0),
        Field("parameters_length", bits=16, default=0, type=int),
        UnknownSizeField("parameters", linked_length_field="parameters_length")
    ]

    def __repr__(self):
        return "{}(pdu={}, ctype={})".format(self.__class__.__name__,
                                             self.pdu_id,
                                             self.ctype)


class BrowsingPacket(Packet):
    BASE_PACKET = AVRTPPacket
    FIELDS = [
        Field("pdu_id", bits=8, type=PDU),
        Field("parameters_length", bits=16, default=0, type=int),
        UnknownSizeField("parameters", linked_length_field="parameters_length")
    ]

    def __repr__(self):
        return "{}(pdu={})".format(self.__class__.__name__,
                                   self.pdu_id)


if __name__ == '__main__':
    packet = ControlPacket(pdu_id=0x74,
                           parameters=["\x03",
                                       "\x00\x00\x00\x00\x00\x00\x00\x01",
                                       "\x00\x02"]) / AVRTPPacket(seq=0, cr=0)

    unpacked = ControlPacket.unpack(packet.pack())
