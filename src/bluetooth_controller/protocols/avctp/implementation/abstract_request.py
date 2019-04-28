try:
    from functools import lru_cache
except ImportError:
    from backports.functools_lru_cache import lru_cache

from .parameter import Parameter
from .base_structure import Structure
from .core.structure import PassThroughPacket, AVCPacket
from .core.structure import ControlPacket, AVRTPPacket, BrowsingPacket

REGISTERED_REQUESTS = {}
REGISTERED_RESPONSES = {}


@lru_cache()
def get_loaded_messages_types(original_classes, key):
    def is_sub_class_of_all(kls, classes):
        return all(issubclass(kls, k) for k in classes)

    def get_loaded(original_classes, current):
        to_ret = {}
        classes = current.__subclasses__()
        for kls in classes:
            if is_sub_class_of_all(kls, original_classes):
                if hasattr(kls, key):
                    to_ret[getattr(kls, key)] = kls

        for kls in classes:
            to_ret.update(get_loaded(original_classes, kls))

        return to_ret

    to_ret = {}
    for k in original_classes:
        to_ret.update(get_loaded(original_classes, k))

    return to_ret


# @lru_cache()
# def get_loaded_passthrough_types(message_type):
#     classes = message_type.__subclasses__()
#     to_ret = {kls.OPERATION_ID: kls for kls in classes}
#     for kls in classes:
#         to_ret.update(get_loaded_messages_types(kls))
#     return to_ret


PASSTHROUGH_OPCODE = "\x7C"
VENDOR_OPCODE = "\x00"

VENDOR_ID_FIELD = "pdu_id"
PASSTHROUGH_ID_FIELD = "operation_id"

PASSTHROUGH_FIELD = "operation_id"
VENDOR_FIELD = "PDU"


class AbstractMessage(Structure):
    IS_RESPONSE = 0
    PACKET_TYPE = AVCPacket

    def __init__(self, packet=None, **kwargs):
        super(AbstractMessage, self).__init__(**kwargs)
        self.seq = 0
        self._packet = packet

    def ignore_keys(self):
        to_ret = super(AbstractMessage, self).ignore_keys()
        to_ret.extend(["seq", "_packet", "packet"])
        return to_ret

    @property
    def packet_extra_keys(self):
        return {}

    @property
    def packet(self):
        if self._packet is None:
            params = {
                "parameters": self.pack_params()
            }
            params.update(self.packet_extra_keys)
            return self.PACKET_TYPE(
                **params
            ) / AVRTPPacket(seq=self.seq, cr=self.IS_RESPONSE)

        return self._packet

    @packet.setter
    def packet(self, value):
        self._packet = value

    def pack(self):
        return self.packet.pack()

    def pretty_print(self):
        return self.packet.pretty_print()

    @classmethod
    def get_relavent_kls(cls, raw_packet):
        raise NotImplementedError("This method must be overrided")

    @classmethod
    @lru_cache()
    def unpack(cls, raw_packet):
        unpacked, kls = cls.get_relavent_kls(raw_packet)

        raw_params = unpacked.parameters[0]

        request = kls(packet=unpacked,
                      **cls.unpack_params(raw_params, kls))
        request.seq = unpacked.seq

        return request


class AbstractRequest(AbstractMessage):
    IS_RESPONSE = 0


class AbstractAVCCommand(AbstractMessage):
    PACKET_TYPE = AVCPacket
    CTYPE = None

    @property
    def packet_extra_keys(self):
        return {
            "ctype": self.CTYPE
        }

    @classmethod
    def get_relavent_kls(cls, raw_packet):
        field = {
            PASSTHROUGH_OPCODE: PASSTHROUGH_FIELD,
            VENDOR_OPCODE: VENDOR_FIELD
        }
        id_field = {
            PASSTHROUGH_OPCODE: PASSTHROUGH_ID_FIELD,
            VENDOR_OPCODE: VENDOR_ID_FIELD
        }

        packet_type = {
            PASSTHROUGH_OPCODE: PassThroughPacket,
            VENDOR_OPCODE: ControlPacket
        }

        # AV/C packets
        opcode = raw_packet[5]  # opcode byte
        unpacked = None
        try:
            unpacked = packet_type[opcode].unpack(raw_packet)
            id_field = id_field[opcode]
            id_field_value = getattr(unpacked, id_field)
            handler = get_loaded_messages_types
            key = field[opcode]
            direction_cls = AbstractResponse if unpacked.cr else AbstractRequest
            kls = handler((cls, direction_cls), key)[id_field_value]

        except:
            if unpacked is None:
                unpacked = cls.PACKET_TYPE.unpack(raw_packet)
            kls = cls

        return unpacked, kls


class PassThroughRequest(AbstractAVCCommand, AbstractRequest):
    PACKET_TYPE = PassThroughPacket

    PARAMETERS = [
        Parameter("operation_id", type=int, length=1),
    ]

    @property
    def packet_extra_keys(self):
        return {
            "operation_id": self.operation_id,
        }


class AbstractControlRequest(AbstractAVCCommand, AbstractRequest):
    PACKET_TYPE = ControlPacket
    PDU = None

    @property
    def packet_extra_keys(self):
        extra = super(AbstractControlRequest, self).packet_extra_keys
        extra["pdu_id"] = self.PDU
        return extra


class AbstractBrowsingCommand(AbstractMessage):
    PACKET_TYPE = BrowsingPacket

    @classmethod
    def get_relavent_kls(cls, raw_packet):
        unpacked = cls.PACKET_TYPE.unpack(raw_packet)
        try:
            id_field_value = getattr(unpacked, "pdu_id")
            direction_cls = AbstractResponse if unpacked.cr else AbstractRequest
            kls = get_loaded_messages_types(
                (cls, direction_cls), VENDOR_FIELD)[id_field_value]

        except:
            kls = cls

        return unpacked, kls


class AbstractBrowseRequest(AbstractBrowsingCommand, AbstractRequest):
    PDU = None

    @property
    def packet_extra_keys(self):
        return {
            "pdu_id": self.PDU
        }


class AbstractResponse(AbstractMessage):
    IS_RESPONSE = 1


class PassThroughResponse(AbstractAVCCommand, AbstractResponse):
    PACKET_TYPE = PassThroughPacket
    PARAMETERS = [
        Parameter("operation_id", type=int, length=1),
    ]

    @property
    def packet_extra_keys(self):
        return {
            "operation_id": self.OPERATION_ID,
        }


class AbstractControlResponse(AbstractAVCCommand, AbstractResponse):
    PACKET_TYPE = ControlPacket
    PDU = None

    @property
    def packet_extra_keys(self):
        extra = super(AbstractControlResponse, self).packet_extra_keys
        extra["pdu_id"] = self.PDU
        return extra


class AbstractBrowseResponse(AbstractBrowsingCommand, AbstractResponse):
    PACKET_TYPE = BrowsingPacket
    PDU = None

    @property
    def packet_extra_keys(self):
        return {
            "pdu_id": self.PDU
        }
