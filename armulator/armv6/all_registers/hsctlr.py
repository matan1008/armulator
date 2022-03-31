from armulator.armv6.all_registers.abstract_register import AbstractRegister


class HSCTLR(AbstractRegister):
    """
    Hyp System Control Register
    """

    @property
    def te(self):
        return self[30]

    @te.setter
    def te(self, flag):
        self[30] = flag

    @property
    def ee(self):
        return self[25]

    @ee.setter
    def ee(self, flag):
        self[25] = flag

    @property
    def fi(self):
        return self[21]

    @fi.setter
    def fi(self, flag):
        self[21] = flag

    @property
    def wxn(self):
        return self[19]

    @wxn.setter
    def wxn(self, flag):
        self[19] = flag

    @property
    def i(self):
        return self[12]

    @i.setter
    def i(self, flag):
        self[12] = flag

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
