from bitstring import BitArray


class JMCR(object):
    """
    Jazelle Main Configuration Register
    """

    def __init__(self):
        self.value = BitArray(length=32)

    def set_je(self, flag):
        self.value[31] = flag

    def get_je(self):
        return self.value[31]
