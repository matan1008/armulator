from armulator.armv6.all_registers.abstract_register import AbstractRegister


class TTBCR(AbstractRegister):
    """
    Translation Table Base Control Register
    """

    def __init__(self):
        super(TTBCR, self).__init__()

    def set_eae(self, flag):
        self.value[0] = flag

    def get_eae(self):
        return self.value[0]

    def set_sh1(self, sh1):
        self.value[2:4] = sh1

    def get_sh1(self):
        return self.value[2:4]

    def set_orgn1(self, orgn1):
        self.value[4:6] = orgn1

    def get_orgn1(self):
        return self.value[4:6]

    def set_irgn1(self, irgn1):
        self.value[6:8] = irgn1

    def get_irgn1(self):
        return self.value[6:8]

    def set_epd1(self, flag):
        self.value[8] = flag

    def get_epd1(self):
        return self.value[8]

    def set_a1(self, flag):
        self.value[9] = flag

    def get_a1(self):
        return self.value[9]

    def set_t1sz(self, t1sz):
        self.value[13:16] = t1sz

    def get_t1sz(self):
        return self.value[13:16]

    def set_sh0(self, sh0):
        self.value[18:20] = sh0

    def get_sh0(self):
        return self.value[18:20]

    def set_orgn0(self, orgn0):
        self.value[20:22] = orgn0

    def get_orgn0(self):
        return self.value[20:22]

    def set_irgn0(self, irgn0):
        self.value[22:24] = irgn0

    def get_irgn0(self):
        return self.value[22:24]

    def set_epd0(self, flag):
        self.value[24] = flag

    def get_epd0(self):
        return self.value[24]

    def set_pd1(self, flag):
        self.value[26] = flag

    def get_pd1(self):
        return self.value[26]

    def set_pd0(self, flag):
        self.value[27] = flag

    def get_pd0(self):
        return self.value[27]

    def set_t0sz(self, t0sz):
        self.value[29:32] = t0sz

    def get_t0sz(self):
        return self.value[29:32]

    def set_n(self, n):
        self.value[29:32] = n

    def get_n(self):
        return self.value[29:32]
