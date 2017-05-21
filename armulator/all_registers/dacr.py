from bitstring import BitArray


class DACR(object):
    """
    Domain Access Control Register
    """

    def __init__(self):
        self.value = BitArray(length=32)

    def set_d_n(self, n, d):
        assert n < 16
        self.value[30 - (2 * n):32 - (2 * n)] = d

    def get_d_n(self, n):
        assert n < 16
        return self.value[30 - (2 * n):32 - (2 * n)]
