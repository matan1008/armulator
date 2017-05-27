from bitstring import BitArray


class FPEXC(object):
    """
    Floating-Point Exception Control register
    """

    def __init__(self):
        self.value = BitArray(length=32)

    def set_ex(self, flag):
        self.value[0] = flag

    def get_ex(self):
        return self.value[0]

    def set_en(self, flag):
        self.value[0] = flag

    def get_en(self):
        return self.value[0]
