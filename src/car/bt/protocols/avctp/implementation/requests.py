from list import List
from items import Item
from events import Event
from core import constants
from data_types import Attribute, FolderName
from constants import Scope, AttributeID, PlayStatus, Direction
from parameter import Parameter, ConstantSizeParameter, ComplexParameter
from abstract_request import AbstractControlRequest, AbstractBrowseRequest, \
    AbstractBrowseResponse, AbstractControlResponse


# class PauseRequest(AbstractPassThroughRequest):
#     OPERATION_ID = 0x46
#     CTYPE = constants.CType.CONTROL
#
#
# class PlayRequest(AbstractPassThroughRequest):
#     OPERATION_ID = 0x44
#     CTYPE = constants.CType.CONTROL

class GetElementAttributesRequest(AbstractControlRequest):
    PDU = constants.PDU.GET_ELEMENT_ATTRIBUTES
    CTYPE = constants.CType.STATUS

    PARAMETERS = [
        # current playing index is 0
        Parameter("identifier", type=int, length=8, default=0),
        Parameter("attributes_count", type=int, length=1),
        ConstantSizeParameter("attributes",
                              linked_length_param="attributes_count",
                              length=4, type=AttributeID),
    ]


class GetElementAttributesResponse(AbstractControlResponse):
    PDU = constants.PDU.GET_ELEMENT_ATTRIBUTES
    CTYPE = constants.CType.STATUS

    PARAMETERS = [
        Parameter("attributes_count", type=int, length=1),
        ComplexParameter("attributes", type=List(Attribute),
                         linked_length_param="attributes_count")
    ]


class GetPlayStatusRequest(AbstractControlRequest):
    PDU = constants.PDU.GET_PLAY_STATUS
    CTYPE = constants.CType.STATUS


class GetPlayStatusResponse(AbstractControlResponse):
    PDU = constants.PDU.GET_PLAY_STATUS
    CTYPE = constants.CType.STATUS

    PARAMETERS = [
        Parameter("song_length", type=int, length=4, default=0),
        Parameter("song_position", type=int, length=4, default=0),
        Parameter("play_status", type=PlayStatus, length=1, default=0),
    ]


class PlayItemRequest(AbstractControlRequest):
    PDU = constants.PDU.PLAY_ITEM
    CTYPE = constants.CType.CONTROL

    PARAMETERS = [
        Parameter("scope", type=Scope, length=1),
        Parameter("uid", type=int, length=8),
        Parameter("uid_counter", type=int, length=2),
    ]


class PlayItemResponse(AbstractControlResponse):
    PDU = constants.PDU.PLAY_ITEM
    CTYPE = constants.CType.CONTROL

    PARAMETERS = [
        Parameter("status", type=constants.Error, length=1),
    ]


class SetAddressedPlayerRequest(AbstractControlRequest):
    PDU = constants.PDU.SET_ADDRESSED_PLAYER
    CTYPE = constants.CType.CONTROL

    PARAMETERS = [
        Parameter("player_id", type=int, length=2),
    ]


class SetAddressedPlayerResponse(AbstractControlResponse):
    PDU = constants.PDU.SET_ADDRESSED_PLAYER
    CTYPE = constants.CType.CONTROL

    PARAMETERS = [
        Parameter("status", type=constants.Error, length=1),
    ]


class NotificationRequest(AbstractControlRequest):
    PDU = constants.PDU.REGISTER_NOTIFICATION
    CTYPE = constants.CType.NOTIFY

    PARAMETERS = [
        Parameter("event_id", type=constants.EventID, length=1),
        Parameter("playback_inverval", type=int, length=4, default=0),
    ]


class NotificationResponse(AbstractControlResponse):
    PDU = constants.PDU.REGISTER_NOTIFICATION
    CTYPE = constants.CType.NOTIFY

    PARAMETERS = [
        ComplexParameter("event", type=Event, linked_length_param=None)
    ]


class ChangePathRequest(AbstractBrowseRequest):
    PDU = constants.PDU.CHANGE_PATH

    PARAMETERS = [
        Parameter("uid_counter", type=int, length=2),
        Parameter("direction", type=Direction, length=1),
        Parameter("uid", type=int, length=8),
    ]


class ChangePathResponse(AbstractBrowseResponse):
    PDU = constants.PDU.CHANGE_PATH

    PARAMETERS = [
        Parameter("status", type=constants.Error, length=1),
        Parameter("number_of_items", type=int, length=4),
    ]


class GetFolderItemsRequest(AbstractBrowseRequest):
    PDU = constants.PDU.GET_FOLDER_ITEMS

    PARAMETERS = [
        Parameter("scope", type=Scope, length=1),
        Parameter("start_item", type=int, length=4),
        Parameter("end_item", type=int, length=4),
        Parameter("attributes_count", type=int, length=1),
        ConstantSizeParameter("attributes",
                              linked_length_param="attributes_count",
                              length=4, type=AttributeID),
    ]


class GetFolderItemsResponse(AbstractBrowseResponse):
    PDU = constants.PDU.GET_FOLDER_ITEMS

    PARAMETERS = [
        Parameter("status", type=constants.Error, length=1),
        Parameter("uid_counter", type=int, length=2),
        Parameter("number_of_items", type=int, length=2),
        ComplexParameter("item_list", type=List(Item),
                         linked_length_param="number_of_items")
    ]


class GetItemAttributesRequest(AbstractBrowseRequest):
    PDU = constants.PDU.GET_ITEM_ATTRIBUTES

    PARAMETERS = [
        Parameter("scope", type=Scope, length=1),
        Parameter("uid", type=int, length=8),
        Parameter("uid_counter", type=int, length=2),
        Parameter("attributes_count", type=int, length=1),
        ConstantSizeParameter("attributes",
                              linked_length_param="attributes_count",
                              length=4, type=AttributeID),
    ]


class GetItemAttributesResponse(AbstractBrowseResponse):
    PDU = constants.PDU.GET_ITEM_ATTRIBUTES

    PARAMETERS = [
        Parameter("status", type=constants.Error, length=1),
        Parameter("attributes_count", type=int, length=1),
        ComplexParameter("attributes", type=List(Attribute),
                         linked_length_param="attributes_count")
    ]


class SetBrowsedPlayerRequest(AbstractBrowseRequest):
    PDU = constants.PDU.SET_BROWSED_PLAYER

    PARAMETERS = [
        Parameter("player_id", type=int, length=2),
    ]


class SetBrowsedPlayerResponse(AbstractBrowseResponse):
    PDU = constants.PDU.SET_BROWSED_PLAYER

    PARAMETERS = [
        Parameter("status", type=constants.Error, length=1),
        Parameter("uid_counter", type=int, length=2),
        Parameter("number_of_items", type=int, length=4),
        Parameter("character_set", type=int, length=2),
        Parameter("folder_depth", type=int, length=1),
        ComplexParameter("folder_names", type=List(FolderName),
                         linked_length_param="folder_depth")
    ]


class GetTotalNumberOfItemsRequest(AbstractBrowseRequest):
    PDU = constants.PDU.GET_TOTAL_NUMBER_OF_ITEMS

    PARAMETERS = [
        Parameter("scope", type=Scope, length=1),
    ]


class GetTotalNumberOfItemsResponse(AbstractBrowseResponse):
    PDU = constants.PDU.GET_TOTAL_NUMBER_OF_ITEMS

    PARAMETERS = [
        Parameter("status", type=constants.Error, length=1),
        Parameter("uid_counter", type=int, length=2),
        Parameter("number_of_items", type=int, length=4),
    ]
