from collections import OrderedDict
from numbers import Number

from backports.functools_lru_cache import lru_cache
from bitarray import bitarray
from enum import Enum

from fields import UnknownSizeField


class Packet(object):
    BASE_PACKET = None
    FIELDS = []

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.assigned_fields = OrderedDict()
        self.layers = []

        self.fields_dict = OrderedDict()
        for field in self.FIELDS:
            self.fields_dict[field.name] = field

        self.initialize_default_fields()
        self.fill_values()
        self.validate_all_present()

    @classmethod
    def create_packet(cls, raw_packet, packet_cls):
        fields = OrderedDict()
        for field in packet_cls.FIELDS:
            temp = bitarray()
            bits = field.bits
            if isinstance(field, UnknownSizeField):
                bits = fields[field.linked_length_field] * 8

            for _ in xrange(bits):
                temp.append(raw_packet.pop(0))

            if bits % 8 == 0 and (field.type is None or not issubclass(field.type, (Number, Enum))):
                if isinstance(field, UnknownSizeField):
                    fields[field.name] = [temp.tobytes()]

                else:
                    fields[field.name] = temp.tobytes()

            else:
                number = 0
                for bit in iter(temp):
                    number = (number << 1) | bit

                try:
                    value = field.type(number) if field.type else number

                except:
                    value = number

                fields[field.name] = value

        return packet_cls(**fields)

    @classmethod
    def _unpack(cls, raw_packet):
        base_packet = None
        if cls.BASE_PACKET:
            base_packet = cls.BASE_PACKET._unpack(raw_packet)

        if base_packet:
            return cls.create_packet(raw_packet, cls) / base_packet

        return cls.create_packet(raw_packet, cls)

    @classmethod
    @lru_cache()
    def unpack(cls, bytes):
        array = bitarray()
        array.frombytes(bytes)

        return cls._unpack(array)

    def pack(self):
        array = bitarray()
        for field in self.fields_dict.values():
            value = getattr(self, field.name)
            field.pack_to(array, value)

        return array.tobytes()

    def pretty_print(self):
        s = ""
        for b in self.pack():
            s += ("%02x" % ord(b)) + " "
        print s

    def validate_all_present(self):
        for field in self.FIELDS:
            if field.default is not None:
                if not hasattr(self, field.name):
                    raise RuntimeError("Required field `{}` is not set!".format(
                        field.name))

    def initialize_default_fields(self):
        for field in self.FIELDS:
            if field.default is not None:
                setattr(self, field.name, field.default)

    def fill_values(self):
        for key, value in self.kwargs.items():
            setattr(self, key, value)

    def __getattr__(self, item):
        return self.assigned_fields[item]

    def __setattr__(self, key, value):
        if key in ["fields_dict", "assigned_fields", "kwargs", "layers"]:
            super(Packet, self).__setattr__(key, value)
            return

        field = self.fields_dict[key]

        if isinstance(field, UnknownSizeField):
            linked_field = self.fields_dict[field.linked_length_field]
            setattr(self, linked_field.name, len("".join(value)))

        field.validate(value)
        self.assigned_fields[key] = value

    def __div__(self, other):
        new_packet = Packet()
        new_packet.layers.append(other)
        new_packet.layers.append(self)
        new_packet.assigned_fields.update(other.assigned_fields)
        new_packet.assigned_fields.update(self.assigned_fields)
        new_packet.fields_dict.update(other.fields_dict)
        new_packet.fields_dict.update(self.fields_dict)

        return new_packet

    def __dir__(self):
        res = dir(type(self)) + list(self.__dict__.keys())
        res.extend(self.fields_dict.keys())
        return res

    def __repr__(self):
        return "{}(layers={})".format(self.__class__.__name__, self.layers)
