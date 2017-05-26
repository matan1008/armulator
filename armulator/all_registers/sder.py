from bitstring import BitArray


class SDER(object):
    """
    Secure Debug Enable Register
    """

    def __init__(self):
        self.value = BitArray(length=32)

    def set_suniden(self, flag):
        self.value[30] = flag

    def get_suniden(self):
        return self.value[30]

    def set_suiden(self, flag):
        self.value[31] = flag

    def get_suiden(self):
        return self.value[31]
