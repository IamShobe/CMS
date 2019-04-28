from bitarray import bitarray


def to_number(bytes):
    temp = bitarray()
    temp.frombytes(bytes)
    number = 0
    for bit in iter(temp):
        number = (number << 1) | bit

    return number


def get_linked_item(id, kls):
    classes = kls.__subclasses__()
    for sub_kls in classes:
        if id == sub_kls.TYPE_ID:
            return sub_kls

        if len(sub_kls.__subclasses__()) > 0:
            ret_val = get_linked_item(id, sub_kls)
            if ret_val:
                return ret_val


