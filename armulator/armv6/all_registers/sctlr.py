from armulator.armv6.all_registers.abstract_register import AbstractRegister


class SCTLR(AbstractRegister):
    """
    System Control Register
    """

    @property
    def ie(self):
        return self[31]

    @ie.setter
    def ie(self, flag):
        self[31] = flag

    @property
    def te(self):
        return self[30]

    @te.setter
    def te(self, flag):
        self[30] = flag

    @property
    def afe(self):
        return self[29]

    @afe.setter
    def afe(self, flag):
        self[29] = flag

    @property
    def tre(self):
        return self[28]

    @tre.setter
    def tre(self, flag):
        self[28] = flag

    @property
    def nmfi(self):
        return self[27]

    @nmfi.setter
    def nmfi(self, flag):
        self[27] = flag

    @property
    def ee(self):
        return self[25]

    @ee.setter
    def ee(self, flag):
        self[25] = flag

    @property
    def ve(self):
        return self[24]

    @ve.setter
    def ve(self, flag):
        self[24] = flag

    @property
    def u(self):
        return self[22]

    @u.setter
    def u(self, flag):
        self[22] = flag

    @property
    def fi(self):
        return self[21]

    @fi.setter
    def fi(self, flag):
        self[21] = flag

    @property
    def uwxn(self):
        return self[20]

    @uwxn.setter
    def uwxn(self, flag):
        self[20] = flag

    @property
    def wxn(self):
        return self[19]

    @wxn.setter
    def wxn(self, flag):
        self[19] = flag

    @property
    def dz(self):
        return self[19]

    @dz.setter
    def dz(self, flag):
        self[19] = flag

    @property
    def ha(self):
        return self[17]

    @ha.setter
    def ha(self, flag):
        self[17] = flag

    @property
    def br(self):
        return self[17]

    @br.setter
    def br(self, flag):
        self[17] = flag

    @property
    def rr(self):
        return self[14]

    @rr.setter
    def rr(self, flag):
        self[14] = flag

    @property
    def v(self):
        return self[13]

    @v.setter
    def v(self, flag):
        self[13] = flag

    @property
    def i(self):
        return self[12]

    @i.setter
    def i(self, flag):
        self[12] = flag

    @property
    def z(self):
        return self[11]

    @z.setter
    def z(self, flag):
        self[11] = flag

    @property
    def sw(self):
        return self[10]

    @sw.setter
    def sw(self, flag):
        self[10] = flag

    @property
    def b(self):
        return self[7]

    @b.setter
    def b(self, flag):
        self[7] = flag

    @property
    def cp15ben(self):
        return self[5]

    @cp15ben.setter
    def cp15ben(self, flag):
        self[5] = flag

    @property
    def c(self):
        return self[2]

    @c.setter
    def c(self, flag):
        self[2] = flag

    @property
    def a(self):
        return self[1]

    @a.setter
    def a(self, flag):
        self[1] = flag

    @property
    def m(self):
        return self[0]

    @m.setter
    def m(self, flag):
        self[0] = flag
