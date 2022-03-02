from armulator.armv6.all_registers.abstract_register import AbstractRegister
from armulator.armv6.bits_ops import chain, bit_at, substring


class CPSR(AbstractRegister):
    """
    Current Program Status Register
    """

    @property
    def n(self):
        return self[31]

    @n.setter
    def n(self, flag):
        self[31] = flag

    @property
    def z(self):
        return self[30]

    @z.setter
    def z(self, flag):
        self[30] = flag

    @property
    def c(self):
        return self[29]

    @c.setter
    def c(self, flag):
        self[29] = flag

    @property
    def v(self):
        return self[28]

    @v.setter
    def v(self, flag):
        self[28] = flag

    @property
    def q(self):
        return self[27]

    @q.setter
    def q(self, flag):
        self[27] = flag

    @property
    def j(self):
        return self[24]

    @j.setter
    def j(self, flag):
        self[24] = flag

    @property
    def ge(self):
        return self[19:16]

    @ge.setter
    def ge(self, ge):
        self[19:16] = ge

    @property
    def it(self):
        return chain(self[15:10], self[26:25], 2)

    @it.setter
    def it(self, it):
        self[15:10] = substring(it, 7, 2)
        self[26:25] = substring(it, 1, 0)

    @property
    def e(self):
        return self[9]

    @e.setter
    def e(self, flag):
        self[9] = flag

    @property
    def a(self):
        return self[8]

    @a.setter
    def a(self, flag):
        self[8] = flag

    @property
    def i(self):
        return self[7]

    @i.setter
    def i(self, flag):
        self[7] = flag

    @property
    def f(self):
        return self[6]

    @f.setter
    def f(self, flag):
        self[6] = flag

    @property
    def t(self):
        return self[5]

    @t.setter
    def t(self, flag):
        self[5] = flag

    @property
    def m(self):
        return self[4:0]

    @m.setter
    def m(self, mode):
        self[4:0] = mode

    @property
    def isetstate(self):
        return chain(self[24], self[5], 1)

    @isetstate.setter
    def isetstate(self, isetstate):
        self[24] = bit_at(isetstate, 1)
        self[5] = bit_at(isetstate, 0)

    @property
    def apsr(self):
        return self.value & 0xF80F0000
