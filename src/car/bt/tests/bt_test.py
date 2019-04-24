import bluetooth


def read_until_cr(s, max_c=100):
    buffer = ""
    current_c = 0
    try:
        while current_c < max_c:
            byte = s.recv(1)
            buffer += byte
            current_c += 1
            if byte in ["\n", "\r"]:
                if buffer.strip() != "":
                    break

    except:
        pass

    return buffer.strip()


def read_until_ok(s):
    buffer = ""
    while True:
        current = read_until_cr(s)
        buffer += current + "\n"
        if current == "OK":
            break

        elif current == "ERROR":
            current = read_until_cr(s)
            buffer += current + "\n"
            break

    return buffer



def write_message(s, msg):
    print "writing: {}".format(msg)
    s.send("{}\r".format(msg))


if __name__ == '__main__':
    hw = "C0:EE:FB:D5:FC:A2"
    s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    s.connect((hw, 3))



    write_message(s, "AT+BRSF=3943")
    print read_until_ok(s)

    write_message(s, "AT+CIND=?")
    print read_until_ok(s)

    write_message(s, "AT+CIND?")
    print read_until_ok(s)

    write_message(s, "AT+CMER=3,0,0,1")
    print read_until_ok(s)

    write_message(s, "AT+CMEE=1")
    print read_until_ok(s)

    # write_message(s, "AT+CMER=3,1,0,0,0")
    # print read_until_ok(s)

    write_message(s, "AT+BIA=1,1,1,1,1,1,1")
    print read_until_ok(s)

    write_message(s, "AT+CLIP=1")
    print read_until_ok(s)

    write_message(s, "AT+CCWA=1")
    print read_until_ok(s)

    write_message(s, "AT+CHLD=?")
    print read_until_ok(s)

    write_message(s, "AT+BIND=1,2")
    print read_until_ok(s)

    write_message(s, "AT+BIND=?")
    print read_until_ok(s)

    write_message(s, "AT+BIND?")
    print read_until_ok(s)

    write_message(s, "AT+CLCC")
    print read_until_ok(s)

    # write_message(s, "ATA")  # Answer
    # print read_until_ok(s)
    # write_message(s, "AT+CHUP")  # HUNG UP
    # print read_until_ok(s)

    #
    # while True:
    #     write_message(s, "AT+CIND?")
    #     print read_until_cr(s)
    #     print read_until_cr(s)

    while True:
        print read_until_cr(s)

    s.close()
