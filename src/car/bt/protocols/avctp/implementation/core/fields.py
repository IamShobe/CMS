from enum import Enum

MASKS = {
    0: 1,
}
MAX_MASK = 32


def create_masks():
    for i in xrange(1, MAX_MASK):
        MASKS[i] = MASKS[i - 1] * 2

create_masks()


class Field(object):
    def __init__(self, name, bits, default=None, type=None):
        self.name = name
        self.bits = bits
        self.default = default
        self.type = type

    def validate(self, value):
        if issubclass(type(value), Enum):
            value = value.value

        max_value = 2 ** self.bits - 1
        if self.bits % 8 != 0 and isinstance(value, basestring):
            raise RuntimeError(
                "Field:`{}`, Invalid value given: {}, "
                "type is str and bits does not fit {} % 8 != 0".format(
                    self.name, value, self.bits))

        if value > max_value and not isinstance(value, basestring):
            raise RuntimeError("Field:`{}`, Invalid value given: {!r} max is {}".format(
                self.name, value, max_value))

        return True

    def pack_to(self, bitarray, value):
        if issubclass(type(value), Enum):
            value = value.value

        self.validate(value)
        if self.bits % 8 == 0 and isinstance(value, basestring):
            bitarray.frombytes(value)
            return

        for i in xrange(self.bits-1, -1, -1):
            bit = (MASKS[i] & value > 0)
            bitarray.append(bit)

    def __repr__(self):
        return "{}(name={!r}, bits={!r})".format(self.__class__.__name__,
                                                 self.name, self.bits)


class UnknownSizeField(Field):
    def __init__(self, name, linked_length_field):
        super(UnknownSizeField, self).__init__(name, None, default=[])
        self.linked_length_field = linked_length_field

    def validate(self, value):
        return True

    def pack_to(self, bitarray, value):
        if issubclass(type(value), Enum):
            value = value.value

        bitarray.frombytes("".join(value))
