from enum import Enum


# ------------ SCOPE -----------
class Scope(Enum):
    MEDIA_PLAYER = 0x00
    VIRTUAL_FILESYSTEM = 0x01
    SEARCH = 0x02
    NOW_PLAYING = 0x03


# ------------ ATTRIBUTES -----------
class Attribute(Enum):
    NOT_USED = 0x0
    TITLE = 0x1
    ARTIST_NAME = 0x2
    ALBUM_NAME = 0x3
    TRACK_NUMBER = 0x4
    TOTAL_NUMBER_OF_TRACKS = 0x5
    GENRE = 0x6
    PLAYING_TIME = 0x7
    DEFAULT_COVER_ART = 0x8


# ------------ Item Types -----------
class ItemType(Enum):
    MEDIA_PLAYER = 0x1
    FOLDER_ITEM = 0x2
    MEDIA_ELEMENT = 0x3


# ------------ Play Status -----------
class PlayStatus(Enum):
    STOPPED = 0x0
    PLAYING = 0x1
    PAUSED = 0x2
    FWD_SEEK = 0x3
    REV_SEEK = 0x4


# ---------- PLAYER TYPES ----------
class MajorPlayerType(Enum):
    AUDIO = 0x1
    VIDEO = 0x2
    BROADCAST_AUDIO = 0x4
    BROADCAST_VIDEO = 0x8


# -------- Media Types ----------
class MediaType(Enum):
    AUDIO = 0x1
    VIDEO = 0x2


# --------- PLAYER SUB TYPES -----------
class SubPlayerType(Enum):
    NONE = 0x0
    AUDIO_BOOK = 0x1
    PODCAST = 0x2


# ----------- Folder TYPES ------------
class FolderType(Enum):
    MIXED = 0x0
    TITLES = 0x1
    ALBUMS = 0x2
    ARTISTS = 0x3
    GENRES = 0x4
    PLAYLISTS = 0x5
    YEARS = 0x6


# -------- Bool ------------
class Bool(Enum):
    NO = 0x0
    YES = 0x1

