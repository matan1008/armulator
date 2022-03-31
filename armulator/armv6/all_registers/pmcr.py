from armulator.armv6.all_registers.abstract_register import AbstractRegister


class PMCR(AbstractRegister):
    """
    Performance Monitors Control Register
    """

    @property
    def e(self):
        return self[0]

    @e.setter
    def e(self, flag):
        self[0] = flag

    @property
    def p(self):
        return self[1]

    @p.setter
    def p(self, flag):
        self[1] = flag

    @property
    def c(self):
        return self[2]

    @c.setter
    def c(self, flag):
        self[2] = flag

    @property
    def d(self):
        return self[3]

    @d.setter
    def d(self, flag):
        self[3] = flag

    @property
    def x(self):
        return self[4]

    @x.setter
    def x(self, flag):
        self[4] = flag

    @property
    def dp(self):
        return self[5]

    @dp.setter
    def dp(self, flag):
        self[5] = flag

    @property
    def imp(self):
        return self[31:24]

    @imp.setter
    def imp(self, imp):
        self[31:24] = imp

    @property
    def idcode(self):
        return self[23:16]

    @idcode.setter
    def idcode(self, idcode):
        self[23:16] = idcode

    @property
    def n(self):
        return self[15:11]

    @n.setter
    def n(self, n):
        self[15:11] = n
