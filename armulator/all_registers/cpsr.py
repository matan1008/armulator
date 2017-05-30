from bitstring import BitArray


class CPSR(object):
    """
    Current Program Status Register
    """

    def __init__(self):
        self.value = BitArray(length=32)

    def set_n(self, flag):
        if type(flag) is not bool:
            flag = flag == "1"
        self.value[0] = flag

    def get_n(self):
        return self.value[0]

    def set_z(self, flag):
        if type(flag) is not bool:
            flag = flag == "1"
        self.value[1] = flag

    def get_z(self):
        return self.value[1]

    def set_c(self, flag):
        if type(flag) is not bool:
            flag = flag == "1"
        self.value[2] = flag

    def get_c(self):
        return self.value[2]

    def set_v(self, flag):
        if type(flag) is not bool:
            flag = flag == "1"
        self.value[3] = flag

    def get_v(self):
        return self.value[3]

    def set_q(self, flag):
        if type(flag) is not bool:
            flag = flag == "1"
        self.value[4] = flag

    def get_q(self):
        return self.value[4]

    def set_j(self, flag):
        self.value[7] = flag

    def get_j(self):
        return self.value[7]

    def set_ge(self, ge):
        self.value[12:16] = ge

    def get_ge(self):
        return self.value[12:16]

    def set_it(self, it):
        self.value[16:22] = it[0:6]
        self.value[5:7] = it[6:8]

    def get_it(self):
        return self.value[16:22] + self.value[5:7]

    def set_e(self, flag):
        self.value[22] = flag

    def get_e(self):
        return self.value[22]

    def set_a(self, flag):
        self.value[23] = flag

    def get_a(self):
        return self.value[23]

    def set_i(self, flag):
        self.value[24] = flag

    def get_i(self):
        return self.value[24]

    def set_f(self, flag):
        self.value[25] = flag

    def get_f(self):
        return self.value[25]

    def set_t(self, flag):
        self.value[26] = flag

    def get_t(self):
        return self.value[26]

    def set_m(self, mode):
        self.value[27:32] = mode

    def get_m(self):
        return self.value[27:32]

    def set_isetstate(self, isetstate):
        self.value[7] = isetstate[0]
        self.value[26] = isetstate[1]

    def get_isetstate(self):
        return BitArray(bool=self.value[7]) + BitArray(bool=self.value[26])

    def get_apsr(self):
        return self.value & "0xF80F0000"
