from armulator.armv6.all_registers.abstract_register import AbstractRegister


class TTBCR(AbstractRegister):
    """
    Translation Table Base Control Register
    """

    @property
    def eae(self):
        return self[31]

    @eae.setter
    def eae(self, flag):
        self[31] = flag

    @property
    def sh1(self):
        return self[29:28]

    @sh1.setter
    def sh1(self, sh1):
        self[29:28] = sh1

    @property
    def orgn1(self):
        return self[27:26]

    @orgn1.setter
    def orgn1(self, orgn1):
        self[27:26] = orgn1

    @property
    def irgn1(self):
        return self[25:24]

    @irgn1.setter
    def irgn1(self, irgn1):
        self[25:24] = irgn1

    @property
    def epd1(self):
        return self[23]

    @epd1.setter
    def epd1(self, flag):
        self[23] = flag

    @property
    def a1(self):
        return self[22]

    @a1.setter
    def a1(self, flag):
        self[22] = flag

    @property
    def t1sz(self):
        return self[18:16]

    @t1sz.setter
    def t1sz(self, t1sz):
        self[18:16] = t1sz

    @property
    def sh0(self):
        return self[13:12]

    @sh0.setter
    def sh0(self, sh0):
        self[13:12] = sh0

    @property
    def orgn0(self):
        return self[11:9]

    @orgn0.setter
    def orgn0(self, orgn0):
        self[11:9] = orgn0

    @property
    def irgn0(self):
        return self[9:8]

    @irgn0.setter
    def irgn0(self, irgn0):
        self[9:8] = irgn0

    @property
    def epd0(self):
        return self[7]

    @epd0.setter
    def epd0(self, flag):
        self[7] = flag

    @property
    def pd1(self):
        return self[5]

    @pd1.setter
    def pd1(self, flag):
        self[5] = flag

    @property
    def pd0(self):
        return self[4]

    @pd0.setter
    def pd0(self, flag):
        self[4] = flag

    @property
    def t0sz(self):
        return self[2:0]

    @t0sz.setter
    def t0sz(self, t0sz):
        self[2:0] = t0sz

    @property
    def n(self):
        return self[2:0]

    @n.setter
    def n(self, n):
        self[2:0] = n
