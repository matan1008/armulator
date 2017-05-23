from bitstring import BitArray


class TEECR(object):
    """
    ThumbEE Configuration Register
    """

    def __init__(self):
        self.value = BitArray(length=32)

    def set_xed(self, flag):
        self.value[31] = flag

    def get_xed(self):
        return self.value[31]
