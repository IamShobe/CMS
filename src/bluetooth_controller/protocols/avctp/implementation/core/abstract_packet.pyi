from backports.functools_lru_cache import lru_cache


class Packet(object):
    BASE_PACKET = None
    FIELDS = []

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.assigned_fields = {}
        self.layers = []
        self.fields_dict = {}

    @classmethod
    def create_packet(cls, raw_packet, packet_cls):
        pass

    @classmethod
    def _unpack(cls, raw_packet):
        pass

    @classmethod
    @lru_cache()
    def unpack(cls, bytes):
        pass

    def pack(self):
        pass

    def pretty_print(self):
        pass

    def validate_all_present(self):
        pass

    def initialize_default_fields(self):
        pass

    def fill_values(self):
        pass

    def __div__(self, other):
        pass
