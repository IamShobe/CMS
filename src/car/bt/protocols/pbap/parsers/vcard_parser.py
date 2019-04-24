import re
import base64
from collections import namedtuple

import vobject

from vcard2to3 import convert


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


ATTR_TRANSLATIONS = {
    "N": Handler(key="name",
                 callback=None,
                 action="assign"),
    "FN": Handler(key="family_name",
                  callback=None,
                  action="assign"),
    "TEL": Handler(key="numbers", callback=handle_tel, action="append"),
    "X-IRMC-CALL-DATETIME": Handler(key="timestamp", callback=handle_time,
                                    action="assign"),
    "PHOTO": Handler(key="photo", callback=None, action="assign"),
    "ADR": Handler(key="address", callback=None, action="assign")
}


class Contact(object):
    def __init__(self, name, full_name=None, numbers=None,
                 photo=None, address=None, **kwargs):
        self.name = str(name)
        self.full_name = \
            full_name.encode("utf-8") if full_name is not None else None
        self.numbers = numbers
        self.photo = base64.b64encode(photo) if photo is not None else None
        self.address = str(address)
        self.kwargs = kwargs

    def to_dict(self):
        return {
            "name": self.name,
            "full_name": self.full_name,
            "numbers": self.numbers,
            "photo": self.photo,
            "address": self.address,
            "kwargs": self.kwargs
        }

    def __repr__(self):
        return "{}({}, numbers={})".format(self.__class__.__name__,
                                           self.name, self.numbers)

    @classmethod
    def create_from_card(cls, card):
        card_attrs = {}

        for child in card.getChildren():
            handler = ATTR_TRANSLATIONS.get(child.name, None)
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

        return cls(**card_attrs)


class CallLog(Contact):
    def __init__(self, name, full_name=None, numbers=None,
                 timestamp=None, **kwargs):
        super(CallLog, self).__init__(name=name, full_name=full_name,
                                      numbers=numbers, **kwargs)
        self.timestamp = timestamp

    def to_dict(self):
        return {
            "name": self.name,
            "family_name": self.full_name,
            "numbers": self.numbers,
            "timestamp": self.timestamp,
            "kwargs": self.kwargs
        }

    def __repr__(self):
        return "{}({}, numbers={}, timestamp={})".format(
            self.__class__.__name__,
            self.name, self.numbers, self.timestamp)


def build_models(book, cls):
    return [cls.create_from_card(card) for card in book]


def parse(vcf_text, cls=Contact):
    raw_book = convert(fix_encoding_issues(vcf_text))
    book = list(vobject.readComponents(raw_book, ignoreUnreadable=True))
    return build_models(book, cls)


if __name__ == '__main__':
    with open("book.vcf", "rb") as f:
        raw_book = f.read()

    json_book = parse(raw_book)
    print repr(json_book)
