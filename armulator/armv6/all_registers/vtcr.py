from armulator.armv6.all_registers.abstract_register import AbstractRegister


class VTCR(AbstractRegister):
    """
    Virtualization Translation Control Register
    """

    @property
    def sh0(self):
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
    def sl0(self):
        return self[7:6]

    @sl0.setter
    def sl0(self, sl0):
        self[7:6] = sl0

    @property
    def s(self):
        return self[4]

    @s.setter
    def s(self, flag):
        self[4] = flag

    @property
    def t0sz(self):
        return self[3:0]

    @t0sz.setter
    def t0sz(self, t0sz):
        self[3:0] = t0sz
