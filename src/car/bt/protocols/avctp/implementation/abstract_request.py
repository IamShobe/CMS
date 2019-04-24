
try:
    from functools import lru_cache
except ImportError:
    from backports.functools_lru_cache import lru_cache

from core.structure import ControlPacket, AVRTPPacket, BrowsingPacket
from base_structure import Structure

REGISTERED_REQUESTS = {}
REGISTERED_RESPONSES = {}


@lru_cache()
def get_loaded_messages_types(message_type):
    classes = message_type.__subclasses__()
    to_ret = {kls.PDU: kls for kls in classes}
    for kls in classes:
        to_ret.update(get_loaded_messages_types(kls))
    return to_ret


class AbstractMessage(Structure):
    PDU = None
    IS_RESPONSE = 0
    PACKET_TYPE = None

    def __init__(self, packet=None, **kwargs):
        super(AbstractMessage, self).__init__(**kwargs)
        self.seq = 0
        self._packet = packet

    def ignore_keys(self):
        to_ret = super(AbstractMessage, self).ignore_keys()
        to_ret.extend(["seq", "_packet"])
        return to_ret

    @property
    def packet_extra_keys(self):
        return {}

    @property
    def packet(self):
        if self._packet is None:
            params = {
                "pdu_id": self.PDU,
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
    def unpack(cls, raw_packet):
        unpacked = cls.PACKET_TYPE.unpack(raw_packet)
        try:
            if unpacked.cr:
                kls = \
                    get_loaded_messages_types(AbstractResponse)[unpacked.pdu_id]
            else:
                kls = \
                    get_loaded_messages_types(AbstractRequest)[unpacked.pdu_id]

        except:
            kls = cls

        raw_params = unpacked.parameters[0]

        request = kls(packet=unpacked,
                      **cls.unpack_params(raw_params, kls))
        request.seq = unpacked.seq

        return request


class AbstractRequest(AbstractMessage):
    IS_RESPONSE = 0


class AbstractControlRequest(AbstractRequest):
    PACKET_TYPE = ControlPacket
    CTYPE = None

    @property
    def packet_extra_keys(self):
        return {
            "ctype": self.CTYPE
        }


class AbstractBrowseRequest(AbstractRequest):
    PACKET_TYPE = BrowsingPacket


class AbstractResponse(AbstractMessage):
    IS_RESPONSE = 1


class AbstractControlResponse(AbstractResponse):
    PACKET_TYPE = ControlPacket
    CTYPE = None

    @property
    def packet_extra_keys(self):
        return {
            "ctype": self.CTYPE
        }


class AbstractBrowseResponse(AbstractResponse):
    PACKET_TYPE = BrowsingPacket
