from backports.functools_lru_cache import lru_cache

from constants import AttributeID
from base_structure import Structure
from parameter import Parameter, SingleUnknownSizeParameter


class FolderName(Structure):
    PARAMETERS = [
        Parameter("name_length", type=int, length=2),
        SingleUnknownSizeParameter("name", linked_length_param="name_length"),
    ]


class Attribute(Structure):
    PARAMETERS = [
        Parameter("id", type=AttributeID, length=4),
        Parameter("character_set", type=int, length=2),
        Parameter("value_length", type=int, length=2),
        SingleUnknownSizeParameter("value", linked_length_param="value_length"),
    ]

    def pack(self):
        return "".join(self.pack_params())

    @classmethod
    @lru_cache()
    def unpack(cls, value, counter=None):
        return cls(**cls.unpack_params(value, counter=counter))
