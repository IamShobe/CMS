from .connection import Connection
from .implementation.core.constants import Error, EventID
from ..abstract_controller import ProtocolController


class AVCTPController(ProtocolController):
    SERVICE_CLASS = "110E"

    def _connect(self, port):
        connection = Connection(self.address, control_port=port)
        connection.connect()
        return connection

    def _close(self):
        self.connection.close()


if __name__ == '__main__':
    address = "C0:EE:FB:D5:FC:A2"
    port = 23
    conn = AVCTPController(address)
    conn.connect(port)

    # conn.connection.get_total_number_of_items(Scope.MEDIA_PLAYER)
    resp = conn.connection.list_media_players()
    assert resp.status == Error.SUCCESS
    player = resp.item_list[0]
    player_id = player.player_id
    # print player.features_mask
    # print player.name
    resp = conn.connection.set_browsed_player(player_id)
    assert resp.status == Error.SUCCESS
    resp = conn.connection.set_addressed_player(player_id)
    assert resp.status == Error.SUCCESS

    # time.sleep(3)
    # conn.connection.play()
    #
    # time.sleep(3)
    # conn.connection.pause()
    #
    # time.sleep(3)
    # conn.connection.stop()
    #
    # time.sleep(3)
    # conn.connection.next_song()
    #
    # time.sleep(3)
    # conn.connection.prev_song()
    #
    # time.sleep(3)
    # abc = conn.connection.skip()

    abc = conn.connection.list_played_items()

    # for item in abc.item_list:
    #     print "Song Name: {}".format(item.name)
    #     for attribute in item.attributes:
    #         print "{!r}: {!r}".format(attribute.id, attribute.value)

    playing = conn.connection.get_track_info()
    # print ""
    # print "Currenty playing song details:"
    # for attribute in playing.attributes:
    #     print "{!r}: {!r}".format(attribute.id, attribute.value)

    item = conn.connection.get_play_status()
    # print "Status: {!r}".format(item.play_status)
    # print "Current Position: {}/{}".format(item.song_position, item.song_length)

    event = conn.connection.register_event(EventID.TRACK_CHANGED)
    item = conn.connection.get_track_image_of(event.event.identifier)
    item2 = conn.connection.get_current_track_image()

    # print conn.connection.unhandled_messages
    conn.close()

    # request = PlayItemRequest(scope=0, uid=1, uid_counter=0)
    # browse_request = GetFolderItemsRequest(scope=Scope.NOW_PLAYING,
    #                                        start_item=0,
    #                                        end_item=3,
    #                                        attribute_count=0)
    #
    # packed = request.pack()
    # unpacked = PlayItemRequest.unpack(packed)
    # browse_request.pretty_print()
