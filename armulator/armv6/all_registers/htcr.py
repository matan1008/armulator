from armulator.armv6.all_registers.abstract_register import AbstractRegister


class HTCR(AbstractRegister):
    """
    Hyp Translation Control Register
    """

    @property
    def sh0(self) -> int:
        return self[13:12]

    @sh0.setter
    def sh0(self, sh0):
        self[13:12] = sh0

    @property
    def orgn0(self):
        return self[11:10]

    @orgn0.setter
    def orgn0(self, orgn0):
        self[11:10] = orgn0

    @property
    def irgn0(self):
        return self[9:8]

    @irgn0.setter
    def irgn0(self, irgn0):
        self[9:8] = irgn0

    @property
    def t0sz(self):
        return self[2:0]

    @t0sz.setter
    def t0sz(self, t0sz):
        self[2:0] = t0sz
