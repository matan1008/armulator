from bitstring import BitArray


class VBAR(object):
    """
    Vector Base Address Register
    """

    def __init__(self):
        self.value = BitArray(length=32)

    def set_base_address(self, base_address):
        self.value[0:27] = base_address

    def get_base_address(self):
        return self.value[0:27]
