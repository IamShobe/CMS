from backports.functools_lru_cache import lru_cache

from list import List
from data_types import Attribute
from utils import get_linked_item
from base_structure import Structure
from parameter import Parameter, SingleUnknownSizeParameter, ComplexParameter
from constants import ItemType, MajorPlayerType, SubPlayerType, PlayStatus, \
    FolderType, Bool, MediaType


class Item(Structure):
    PARAMETERS = [
        Parameter("item_type", type=ItemType, length=1),
        Parameter("item_length", type=int, length=2),
    ]

    def pack(self):
        return "".join(self.pack_params())

    @classmethod
    @lru_cache()
    def unpack(cls, value, counter=None):
        unpacked = cls.unpack_params(value)
        counter.max_length = unpacked["item_length"]
        linked = get_linked_item(unpacked["item_type"], cls)
        kwargs = linked.unpack_params(value, counter=counter)
        return linked(**kwargs)


class ItemClass(Item):
    TYPE_ID = None
    ITEM_PARAMETERS = []

    @classmethod
    def get_all_params(cls):
        return cls.PARAMETERS + cls.ITEM_PARAMETERS


class MediaPlayerItem(ItemClass):
    TYPE_ID = ItemType.MEDIA_PLAYER
    ITEM_PARAMETERS = [
        Parameter("player_id", type=int, length=2),
        Parameter("major_player_type", type=MajorPlayerType, length=1),
        Parameter("sub_player_type", type=SubPlayerType, length=4),
        Parameter("play_status", type=PlayStatus, length=1),
        Parameter("features_mask", type=int, length=16),

        Parameter("character_set", type=int, length=2),
        Parameter("name_length", type=int, length=2),
        SingleUnknownSizeParameter("name", linked_length_param="name_length"),
    ]


class FolderItem(ItemClass):
    TYPE_ID = ItemType.FOLDER_ITEM
    ITEM_PARAMETERS = [
        Parameter("uid", type=int, length=8),
        Parameter("folder_type", type=FolderType, length=1),
        Parameter("is_playable", type=Bool, length=1),
        Parameter("character_set", type=int, length=2),
        Parameter("name_length", type=int, length=2),
        SingleUnknownSizeParameter("name", linked_length_param="name_length"),
    ]


class MediaElement(ItemClass):
    TYPE_ID = ItemType.MEDIA_ELEMENT
    ITEM_PARAMETERS = [
        Parameter("uid", type=int, length=8),
        Parameter("media_type", type=MediaType, length=1),
        Parameter("character_set", type=int, length=2),
        Parameter("name_length", type=int, length=2),
        SingleUnknownSizeParameter("name", linked_length_param="name_length"),
        Parameter("attributes_count", type=int, length=1),
        ComplexParameter("attributes", type=List(Attribute),
                         linked_length_param="attributes_count")
    ]
