from armulator.armv6.all_registers.abstract_register import AbstractRegister


class VTCR(AbstractRegister):
    """
    Virtualization Translation Control Register
    """

    def __init__(self):
        super(VTCR, self).__init__()

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

    def set_sl0(self, sl0):
        self.value[24:26] = sl0

    def get_sl0(self):
        return self.value[24:26]

    def set_s(self, flag):
        self.value[27] = flag

    def get_s(self):
        return self.value[27]

    def set_t0sz(self, t0sz):
        self.value[28:32] = t0sz

    def get_t0sz(self):
        return self.value[28:32]
