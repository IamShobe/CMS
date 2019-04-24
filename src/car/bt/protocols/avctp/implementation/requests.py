from abstract_request import AbstractControlRequest, AbstractBrowseRequest, \
    AbstractBrowseResponse, AbstractControlResponse
from complex import List, Item, FolderName
from core import constants
from constants import Scope, Attribute
from parameter import Parameter, ConstantSizeParameter, ComplexParameter


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
        Parameter("event_id", type=constants.Event, length=1),
        Parameter("playback_inverval", type=int, length=4, default=0),
    ]


class NotificationResponse(AbstractControlResponse):
    PDU = constants.PDU.REGISTER_NOTIFICATION
    CTYPE = constants.CType.NOTIFY

    PARAMETERS = [
        Parameter("event_id", type=constants.Event, length=1),
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
                              type=Attribute),
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
