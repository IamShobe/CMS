import re
from collections import namedtuple

import vobject

from car.bt.protocols.pbap import convert


def fix_encoding_issues(text):
    return re.sub(r"=[\n\r]+=", r"=", text)


TelephoneNumber = namedtuple("TelephoneNumber", ["type", "number"])
Handler = namedtuple("Handler", ["key", "callback", "action"])


def handle_tel(child):
    type = child.params["TYPE"][0] if "TYPE" in child.params else "Mobile"
    return TelephoneNumber(type=type, number=child.value)


def handle_time(child):
    return {
        "time": child.value,
        "type": child.params["TYPE"][0]
    }


class CallLog(object):
    ATTR_TRANSLATIONS = {
        "N": Handler(key="name", callback=None, action="assign"),
        "FN": Handler(key="family_name", callback=None, action="assign"),
        "TEL": Handler(key="numbers", callback=handle_tel, action="append"),
        "X-IRMC-CALL-DATETIME": Handler(key="timestamp", callback=handle_time,
                                        action="assign")
    }

    def __init__(self, name, full_name=None, numbers=None,
                 timestamp=None, **kwargs):
        self.name = str(name)
        self.full_name = \
            str(full_name) if full_name is not None else None
        self.numbers = numbers
        self.timestamp = timestamp
        self.kwargs = kwargs

    def to_dict(self):
        return {
            "name": self.name,
            "family_name": self.full_name,
            "numbers": self.numbers,
            "timestamp": self.timestamp,
            "kwargs": self.kwargs
        }

    def __repr__(self):
        return "CallLog({}, numbers={}, timestamp={})".format(
            self.name, self.full_name,
            self.numbers, self.timestamp)

    @classmethod
    def create_from_card(cls, card):
        card_attrs = {}

        for child in card.getChildren():
            handler = cls.ATTR_TRANSLATIONS.get(child.name, None)
            value = child.value
            if handler is not None and handler.callback is not None:
                value = handler.callback(child)

            if handler is None or handler.action == "assign":
                key = child.name if handler is None else handler.key
                card_attrs[key] = value
                continue

            elif handler.action == "append":
                values = card_attrs.get(handler.key, [])
                values.append(value)
                card_attrs[handler.key] = values

        return CallLog(**card_attrs)


def build_models(book):
    return [CallLog.create_from_card(card) for card in book]


def parse(vcf_text):
    raw_book = convert(fix_encoding_issues(vcf_text))
    book = list(vobject.readComponents(raw_book, ignoreUnreadable=True))
    return build_models(book)


if __name__ == '__main__':
    with open("call.log", "rb") as f:
        raw_book = f.read()

    json_book = parse(raw_book)
    import ipdb; ipdb.set_trace()
    print repr(json_book)
