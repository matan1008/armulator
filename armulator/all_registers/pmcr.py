from bitstring import BitArray


class PMCR(object):
    """
    Performance Monitors Control Register
    """

    def __init__(self):
        self.value = BitArray(length=32)

    def set_e(self, flag):
        self.value[31] = flag

    def get_e(self):
        return self.value[31]

    def set_p(self, flag):
        self.value[30] = flag

    def get_p(self):
        return self.value[30]

    def set_c(self, flag):
        self.value[29] = flag

    def get_c(self):
        return self.value[29]

    def set_d(self, flag):
        self.value[28] = flag

    def get_d(self):
        return self.value[28]

    def set_x(self, flag):
        self.value[27] = flag

    def get_x(self):
        return self.value[27]

    def set_dp(self, flag):
        self.value[26] = flag

    def get_dp(self):
        return self.value[26]

    def set_imp(self, imp):
        self.value[0:8] = imp

    def get_imp(self):
        return self.value[0:8]

    def set_idcode(self, idcode):
        self.value[8:16] = idcode

    def get_idcode(self):
        return self.value[8:16]

    def set_n(self, n):
        self.value[16:21] = n

    def get_n(self):
        return self.value[16:21]
