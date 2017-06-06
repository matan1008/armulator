from armulator.all_registers.abstract_register import AbstractRegister


class HTCR(AbstractRegister):
    """
    Hyp Translation Control Register
    """

    def __init__(self):
        super(HTCR, self).__init__()

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

    def set_t0sz(self, t0sz):
        self.value[29:32] = t0sz

    def get_t0sz(self):
        return self.value[29:32]
