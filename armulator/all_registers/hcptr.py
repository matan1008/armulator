from bitstring import BitArray


class HCPTR(object):
    """
    Hyp Coprocessor Trap Register
    """

    def __init__(self):
        self.value = BitArray(length=32)

    def set_tcpac(self, flag):
        self.value[0] = flag

    def get_tcpac(self):
        return self.value[0]

    def set_tta(self, flag):
        self.value[11] = flag

    def get_tta(self):
        return self.value[11]

    def set_tase(self, flag):
        self.value[16] = flag

    def get_tase(self):
        return self.value[16]

    def set_tcp_n(self, n, flag):
        self.value[31 - n] = flag

    def get_tcp_n(self, n):
        return self.value[31 - n]
