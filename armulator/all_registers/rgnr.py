from bitstring import BitArray


class RGNR(object):
    """
    MPU Region Number Register
    """

    def __init__(self, number_of_regions):
        self.value = BitArray(length=32)
        self.n = number_of_regions.bit_length()

    def set_region(self, region):
        self.value[32 - self.n:32] = region

    def get_region(self):
        return self.value[32 - self.n:32]
