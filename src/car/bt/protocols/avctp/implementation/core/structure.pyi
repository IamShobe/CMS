from .abstract_packet import Packet


class AVRTPPacket(Packet):
    seq = None
    avrtp_type = None
    cr = None
    ipid = None
    pid = None

    def __init__(self, seq=None,
                 avrtp_type=None,
                 cr=None,
                 ipid=None,
                 pid=None):
        super(AVRTPPacket, self).__init__()


class AVCPacket(Packet):
    header = None
    ctype = None
    subunit_type = None
    subunit_id = None
    op_code = None

    def __init__(self, header=None,
                 ctype=None,
                 subunit_type=None,
                 subunit_id=None,
                 op_code=None):
        super(AVCPacket, self).__init__()


class PassThroughPacket(Packet):
    header = None
    ctype = None
    subunit_type = None
    subunit_id = None
    op_code = None
    state_flag = None
    operation_id = None
    parameters_length = None
    parameters = None

    def __init__(self, header=None,
                 ctype=None,
                 subunit_type=None,
                 subunit_id=None,
                 op_code=None,
                 state_flag=None,
                 operation_id=None,
                 parameters_length=None,
                 parameters=None):
        super(PassThroughPacket, self).__init__()


class ControlPacket(Packet):
    header = None
    ctype = None
    subunit_type = None
    subunit_id = None
    op_code = None
    company_id = None
    pdu_id = None
    reserved = None
    type = None
    parameters_length = None
    parameters = None

    def __init__(self, header=None,
                 ctype=None,
                 subunit_type=None,
                 subunit_id=None,
                 op_code=None,
                 company_id=None,
                 pdu_id=None,
                 reserved=None,
                 type=None,
                 parameters_length=None,
                 parameters=None):
        super(ControlPacket, self).__init__()


class BrowsingPacket(Packet):
    pdu_id = None
    parameters_length = None
    parameters = None

    def __init__(self, pdu_id=None,
                 parameters_length=None,
                 parameters=None):
        super(BrowsingPacket, self).__init__()
