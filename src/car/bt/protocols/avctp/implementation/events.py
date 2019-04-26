from backports.functools_lru_cache import lru_cache

from parameter import Parameter
from utils import get_linked_item
from core.constants import EventID
from base_structure import Structure
from constants import BatteryStatus, PlayStatus


class Event(Structure):
    PARAMETERS = [
        Parameter("event_id", type=EventID, length=1),
    ]

    def pack(self):
        return "".join(self.pack_params())

    @classmethod
    @lru_cache()
    def unpack(cls, value, counter=None, count=1):
        unpacked = cls.unpack_params(value)
        linked = get_linked_item(unpacked["event_id"], cls)
        kwargs = linked.unpack_params(value, counter=counter)
        return linked(**kwargs)


class EventClass(Event):
    TYPE_ID = None
    ITEM_PARAMETERS = []

    @classmethod
    def get_all_params(cls):
        return cls.PARAMETERS + cls.ITEM_PARAMETERS


class EventPlayBackStatusChanged(EventClass):
    TYPE_ID = EventID.PLAYBACK_STATUS_CHANGED
    ITEM_PARAMETERS = [
        Parameter("play_status", type=PlayStatus, length=8, default=0)
    ]


class EventTrackChanged(EventClass):
    TYPE_ID = EventID.TRACK_CHANGED
    ITEM_PARAMETERS = [
        Parameter("identifier", type=int, length=8, default=0)
    ]


class EventTrackReachedEnd(EventClass):
    TYPE_ID = EventID.TRACK_REACHED_END


class EventTrackReachedStart(EventClass):
    TYPE_ID = EventID.TRACK_REACHED_START


class EventPlayBackPosChanged(EventClass):
    TYPE_ID = EventID.PLAYBACK_POS_CHANGED
    ITEM_PARAMETERS = [
        Parameter("position", type=int, length=4, default=0)
    ]


class EventBattStatusChanged(EventClass):
    TYPE_ID = EventID.BATT_STATUS_CHANGED
    ITEM_PARAMETERS = [
        Parameter("batt_status", type=BatteryStatus, length=1, default=0)
    ]


class EventSystemStatusChanged(EventClass):
    TYPE_ID = EventID.SYSTEM_STATUS_CHANGED
    ITEM_PARAMETERS = [
        Parameter("sys_status", type=int, length=4, default=0)
    ]


class EventPlayerApplicationSettingChanged(EventClass):
    TYPE_ID = EventID.PLAYER_APPLICATION_SETTING_CHANGED


class EventNowPlayingContentChanged(EventClass):
    TYPE_ID = EventID.NOW_PLAYING_CONTENT_CHANGED


class EventAvailablePlayersChanged(EventClass):
    TYPE_ID = EventID.AVAILABLE_PLAYERS_CHANGED


class EventAddressedPlayerChanged(EventClass):
    TYPE_ID = EventID.ADDRESSED_PLAYER_CHANGED


class EventUIDsChanged(EventClass):
    TYPE_ID = EventID.UIDS_CHANGED


class EventVolumeChanged(EventClass):
    TYPE_ID = EventID.VOLUME_CHANGED
