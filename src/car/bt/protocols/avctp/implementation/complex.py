from base_structure import Structure
from parameter import Parameter, SingleUnknownSizeParameter, ComplexParameter
from constants import ItemType, MajorPlayerType, SubPlayerType, PlayStatus, \
    FolderType, Bool, MediaType


def get_linked_item(id, kls):
    classes = kls.__subclasses__()
    for sub_kls in classes:
        if sub_kls.TYPE_ID == id:
            return sub_kls

        if len(sub_kls.__subclasses__()) > 0:
            ret_val = get_linked_item(id, sub_kls)
            if ret_val:
                return ret_val


class List(object):
    class Counter(object):
        def __init__(self):
            self.index = 0

    def __init__(self, type):
        self.type = type

    @classmethod
    def pack(cls, items):
        return "".join(item.pack() for item in items)

    def unpack(self, raw_text, count=1):
        to_ret = []
        current_counter = 0
        current_buffer = raw_text
        for _ in xrange(count):
            c = self.Counter()
            to_ret.append(self.type.unpack(current_buffer, counter=c))
            current_counter += c.index
            current_buffer = current_buffer[current_counter:]

        return to_ret


class Item(Structure):
    PARAMETERS = [
        Parameter("item_type", type=ItemType, length=1),
        Parameter("item_length", type=int, length=2),
    ]

    def pack(self):
        return "".join(self.pack_params())

    @classmethod
    def unpack(cls, value, counter=None):
        unpacked = cls.unpack_params(value)

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


class Attribute(Structure):
    PARAMETERS = [
        Parameter("id", type=int, length=4),
        Parameter("character_set", type=int, length=2),
        Parameter("value_length", type=int, length=2),
        SingleUnknownSizeParameter("value", linked_length_param="value_length"),
    ]

    def pack(self):
        return self.pack_params()

    @classmethod
    def unpack(cls, value, counter=None):
        return cls.unpack_params(value, counter)


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


class FolderName(Structure):
    PARAMETERS = [
        Parameter("name_length", type=int, length=2),
        SingleUnknownSizeParameter("name", linked_length_param="name_length"),
    ]
