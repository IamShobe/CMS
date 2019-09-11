# Capabilities
from enum import Enum


# --------------- CTYPE -------------
class CType(Enum):
    CONTROL = 0
    STATUS = 1
    SPECIFIC_INQUIRY = 2
    NOTIFY = 3
    GENERAL_INQUIRY = 4
    RESPONSE_NOT_IMPLEMENTED = 8
    RESPONSE_ACCEPTED = 9
    RESPONSE_REJECTED = 0xA
    RESPONSE_IN_TRANSITION = 0xb
    RESPONSE_IMPLEMENTED = 0xc
    RESPONSE_CHANGED = 0xd
    RESPONSE_RESERVED = 0xe
    RESPONSE_INTERIM = 0xf


# --------------- PDU -------------
class PDU(Enum):
    # Capabilties
    GET_CAPABILITIES = 0x10

    # Player Application Settings
    LIST_PLAYER_APPLICATION_SETTING_ATTRIBUTES = 0x11
    LIST_PLAYER_APPLICATION_SETTING_VALUES = 0x12
    GET_CURRENT_PLAYER_APPLICATION_SETTING_VALUE = 0x13
    SET_PLAYER_APPLICATION_SETTING_VALUE = 0x14
    GET_PLAYER_APPLICATION_SETTING_ATTRIBUTE_TEXT = 0x15
    GET_PLAYER_APPLICATION_SETTING_VALUE_TEXT = 0x16
    INFORM_DISPLAYABLE_CHARACTER_SET = 0x17
    INFORM_BATTERY_STATUS_OF_CT = 0x18

    # Metadata Attributes for Current Media Item
    GET_ELEMENT_ATTRIBUTES = 0x20

    # Notifications
    GET_PLAY_STATUS = 0x30
    REGISTER_NOTIFICATION = 0x31

    # Continuation
    CONTINUING = 0x40
    # REQUEST_CONTINUING_RESPONSE = 0x40
    # ABORT_CONTINUING_RESPONSE = 0x40

    # Absolute Volume
    SET_ABSOLUTE_VOLUME = 0x50

    # MediaPlayerSelection
    SET_ADDRESSED_PLAYER = 0x60
    GET_FOLDER_ITEMS = 0x71
    GET_TOTAL_NUMBER_OF_ITEMS = 0x75

    # Browsing
    SET_BROWSED_PLAYER = 0x70
    CHANGE_PATH = 0x72
    GET_ITEM_ATTRIBUTES = 0x73
    PLAY_ITEM = 0x74

    # Search
    SEARCH = 0x80

    # Now Playing
    ADD_TO_NOW_PLAYING = 0x90

    # Error Response
    GENERAL_REJECT = 0xa0


# ------------ EVENTS -------------
class EventID(Enum):
    PLAYBACK_STATUS_CHANGED = 0x1
    TRACK_CHANGED = 0x2
    TRACK_REACHED_END = 0x3
    TRACK_REACHED_START = 0x4
    PLAYBACK_POS_CHANGED = 0x5
    BATT_STATUS_CHANGED = 0x6
    SYSTEM_STATUS_CHANGED = 0x7
    PLAYER_APPLICATION_SETTING_CHANGED = 0x8
    NOW_PLAYING_CONTENT_CHANGED = 0x9
    AVAILABLE_PLAYERS_CHANGED = 0xa
    ADDRESSED_PLAYER_CHANGED = 0xb
    UIDS_CHANGED = 0xc
    VOLUME_CHANGED = 0xd

# ------------ ERRORS -------------
class Error(Enum):
    INVALID_COMMAND = 0x00
    INVALID_PARAMETER = 0x01
    PARAMETER_CONTENT_ERROR = 0x02
    INTERNAL_ERROR = 0x03
    SUCCESS = 0x04
    UID_CHANGED = 0x05
    RESERVED = 0x06
    INVALID_DIRECTION = 0x07
    NOT_A_DIRECTORY = 0x08
    DOES_NOT_EXIST = 0x09
    INVALID_SCOPE = 0x0a
    RANGE_OUT_OF_BOUNDS = 0x0b
    FOLDER_ITEM_NOT_PLAYABLE = 0x0c
    MEDIA_IN_USE = 0x0d
    NOW_PLAYING_LIST_FULL = 0x0e
    SEARCH_IN_PROGRESS = 0x10
    INVALID_PLAYER_ID = 0x11
    PLAYER_NOT_BROWSABLE = 0x12
    PLAYER_NOT_ADDRESSED = 0x13
    NO_VALID_SEARCH_RESULTS = 0x14
    NO_AVAILABLE_PLAYERS = 0x15
    ADDRESSED_PLAYER_CHANGED = 0x16


# ------------ PASSTHROUGH -------------
class PassThrough(Enum):
    SKIP = 0x3c
    VOL_UP = 0x41
    VOL_DOWN = 0x42
    MUTE = 0x43
    PLAY = 0x44
    STOP = 0x45
    PAUSE = 0x46
    FORWARD = 0x4b
    BACKWARD = 0x4C