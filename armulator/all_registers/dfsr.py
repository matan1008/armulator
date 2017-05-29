from bitstring import BitArray


class DFSR(object):
    """
    Data Fault Status Register
    """

    def __init__(self):
        self.value = BitArray(length=32)

    def set_cm(self, flag):
        self.value[18] = flag

    def get_cm(self):
        return self.value[18]

    def set_ext(self, flag):
        self.value[19] = flag

    def get_ext(self):
        return self.value[19]

    def set_wnr(self, flag):
        self.value[20] = flag

    def get_wnr(self):
        return self.value[20]

    def set_fs(self, fs):
        self.value[21] = fs[0]
        self.value[28:32] = fs[1:5]

    def get_fs(self):
        return BitArray(bool=self.value[21]) + self.value[28:32]

    def set_lpae(self, flag):
        self.value[22] = flag

    def get_lpae(self):
        return self.value[22]

    def set_domain(self, domain):
        self.value[24:28] = domain

    def get_domain(self):
        return self.value[24:28]

    def set_status(self, status):
        self.value[26:32] = status

    def get_status(self):
        return self.value[26:32]
