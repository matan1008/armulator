from bitstring import BitArray


class CPACR(object):
    """
    Coprocessor Access Control Register
    """

    def __init__(self):
        self.value = BitArray(length=32)

    def set_cp_n(self, n, cp):
        assert n < 14
        self.value[30 - (2 * n):32 - (2 * n)] = cp

    def get_cp_n(self, n):
        assert n < 14
        return self.value[30 - (2 * n):32 - (2 * n)]

    def set_trcdis(self, flag):
        self.value[3] = flag

    def get_trcdis(self):
        return self.value[3]

    def set_d32dis(self, flag):
        self.value[1] = flag

    def get_d32dis(self):
        return self.value[1]

    def set_asedis(self, flag):
        self.value[0] = flag

    def get_asedis(self):
        return self.value[0]
