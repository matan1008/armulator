from armulator.armv6.all_registers.abstract_register import AbstractRegister


class RACR(AbstractRegister):
    """
    Region Access Control Register
    """

    @property
    def xn(self):
        return self[12]

    @xn.setter
    def xn(self, flag):
        self[12] = flag

    @property
    def ap(self):
        return self[10:8]

    @ap.setter
    def ap(self, ap):
        self[10:8] = ap

    @property
    def tex(self):
        return self[5:3]

    @tex.setter
    def tex(self, tex):
        self[5:3] = tex

    @property
    def s(self):
        return self[2]

    @s.setter
    def s(self, flag):
        self[2] = flag

    @property
    def c(self):
        return self[1]

    @c.setter
    def c(self, flag):
        self[1] = flag

    @property
    def b(self):
        return self[0]

    @b.setter
    def b(self, flag):
        self[0] = flag


class DRACR(RACR):
    """
    Data Region Access Control Register
    """
    pass


class IRACR(RACR):
    """
    Instruction Region Access Control Register
    """
    pass
