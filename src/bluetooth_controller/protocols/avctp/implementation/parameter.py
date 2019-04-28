import math

import bitarray
from backports.functools_lru_cache import lru_cache
from enum import Enum

from .utils import to_number


class Parameter(object):
    def __init__(self, name, type, length, callback=False, default=None):
        self.name = name
        self.type = type
        self.length = length
        self.callback = callback
        self.default = default

    def __repr__(self):
        return "{}({!r}, {!r}, length={})".format(
            self.__class__.__name__, self.name,
            self.type, self.length)

    def validate(self, value):
        if issubclass(type(value), Enum):
            value = value.value

        if isinstance(value, basestring):
            if len(value) != self.length:
                raise RuntimeError(
                    "String `{}` is too short! expected length: {}".format(
                        value, self.length))

        else:
            bits_required = 0
            if value != 0:
                bits_required = float(math.ceil(math.log(abs(value), 2)))

            bytes_required = math.ceil(bits_required / 8)
            if bytes_required > self.length:
                raise RuntimeError("Value given is too big! "
                                   "{} doesn't fit in {} bytes".format(
                    value, self.length))

        return True

    def pack(self, value):
        self.validate(value)

        if isinstance(value, basestring):
            return value

        if issubclass(type(value), Enum):
            value = value.value

        array = bitarray.bitarray(bin(value)[2:])
        required_length = self.length * 8
        missing_length = required_length - len(array)
        new_array = bitarray.bitarray("0" * missing_length)
        new_array.extend(array)

        return new_array.tobytes()

    @lru_cache()
    def unpack(self, value, *args, **kwargs):
        if not issubclass(self.type, basestring):
            value = self.type(to_number(value))

        return value


class ConstantSizeParameter(Parameter):
    def __init__(self, name, linked_length_param, type=str, length=1,
                 callback=False):
        super(ConstantSizeParameter, self).__init__(name,
                                                    type=type,
                                                    length=length,
                                                    callback=callback,
                                                    default=[])
        self.linked_length_param = linked_length_param

    def validate(self, value):
        return True

    def pack(self, value):
        return "".join([
            super(ConstantSizeParameter, self).pack(item)
            for item in value
        ])

    @lru_cache()
    def unpack(self, value, *args, **kwargs):
        return [self.type(value[i * self.length, i * self.length + self.length])
                for i in xrange(kwargs["count"])]


class SingleUnknownSizeParameter(Parameter):
    def __init__(self, name, linked_length_param, type=str, length=0,
                 callback=False):
        super(SingleUnknownSizeParameter, self).__init__(name,
                                                         type=type,
                                                         length=length,
                                                         callback=callback,
                                                         default=[])
        self.linked_length_param = linked_length_param

    def validate(self, value):
        return True

    def pack(self, value):
        if issubclass(self.type, basestring):
            return value

        return self.type.pack(value)

    @lru_cache()
    def unpack(self, value, *args, **kwargs):
        if issubclass(self.type, basestring):
            return value

        return self.type.unpack(value)


class ComplexParameter(Parameter):
    def __init__(self, name, linked_length_param, type, length=1,
                 callback=False):
        super(ComplexParameter, self).__init__(name,
                                               type=type,
                                               length=length,
                                               callback=callback,
                                               default=[])
        self.linked_length_param = linked_length_param

    def validate(self, value):
        return True

    def pack(self, value):
        if isinstance(value, list):
            return "".join(item.pack() for item in value)

        return value.pack()

    @lru_cache()
    def unpack(self, value, *args, **kwargs):
        return self.type.unpack(value, *args, **kwargs)
