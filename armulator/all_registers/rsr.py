from bitstring import BitArray


class RSR(object):
    """
    Region Size and Enable Register
    """

    def __init__(self):
        self.value = BitArray(length=32)

    def set_sd_n(self, n, flag):
        self.value[23 - n] = flag

    def get_sd_n(self, n):
        return self.value[23 - n]

    def set_rsize(self, rsize):
        self.value[26:31] = rsize

    def get_rsize(self):
        return self.value[26:31]

    def set_en(self, flag):
        self.value[31] = flag

    def get_en(self):
        return self.value[31]


class DRSR(RSR):
    """
    Data Region Size and Enable Register
    """
    pass


class IRSR(RSR):
    """
    Instruction Region Size and Enable Register
    """
    pass
