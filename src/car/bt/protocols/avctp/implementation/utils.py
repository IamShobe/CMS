from bitarray import bitarray

def to_number(bytes):
    temp = bitarray()
    temp.frombytes(bytes)
    number = 0
    for bit in iter(temp):
        number = (number << 1) | bit

    return number
