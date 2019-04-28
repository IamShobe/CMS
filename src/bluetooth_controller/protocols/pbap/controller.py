from PyOBEX import client, headers, responses

from .parsers import vcard_parser
from ..abstract_controller import ProtocolController


class PBAPController(ProtocolController):
    SERVICE_CLASS = "112F"

    def _connect(self, port):
        obex_client = client.Client(self.address, port)
        uuid = \
            "\x79\x61\x35\xf0\xf0\xc5\x11\xd8\x09\x66\x08\x00\x20\x0c\x9a\x66"
        result = obex_client.connect(header_list=[headers.Target(uuid)])
        if not isinstance(result, responses.ConnectSuccess):
            raise RuntimeError("Failed to connect to phone.")

        return obex_client

    def _close(self):
        self.connection.disconnect()

    def get_phonebook(self):
        self.logger.info("Fetching phonebook...")
        hdrs, cards = self.connection.get(
            "telecom/pb", header_list=[headers.Type("x-bt/phonebook")])
        # with open("book.vcf", 'wb') as f:
        #     f.write(cards)

        return vcard_parser.parse(cards, cls=vcard_parser.Contact)

    def get_history(self):
        hdrs, cards = self.connection.get(
            "/telecom/cch", header_list=[headers.Type("x-bt/phonebook")])

        return vcard_parser.parse(cards, cls=vcard_parser.CallLog)
