from bitstring import BitArray


class SUNAVCR(object):
    """
    Secure User and non-secure Access Validation Control Register
    """

    def __init__(self):
        self.value = BitArray(32)

    def set_v(self, flag):
        self.value[31] = flag

    def get_v(self):
        return self.value[31]
