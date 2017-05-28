from bitstring import BitArray


class HPFAR(object):
    """
    Hyp IPA Fault Address Register
    """

    def __init__(self):
        self.value = BitArray(length=32)

    def set_fipa(self, fipa):
        self.value[0:28] = fipa

    def get_fipa(self):
        return self.value[0:28]
