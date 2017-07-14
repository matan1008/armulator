from armulator.armv6.all_registers.abstract_register import AbstractRegister


class RACR(AbstractRegister):
    """
    Region Access Control Register
    """

    def __init__(self):
        super(RACR, self).__init__()

    def set_xn(self, flag):
        self.value[19] = flag

    def get_xn(self):
        return self.value[19]

    def set_ap(self, ap):
        self.value[21:24] = ap

    def get_ap(self):
        return self.value[21:24]

    def set_tex(self, tex):
        self.value[26:29] = tex

    def get_tex(self):
        return self.value[26:29]

    def set_s(self, flag):
        self.value[29] = flag

    def get_s(self):
        return self.value[29]

    def set_c(self, flag):
        self.value[30] = flag

    def get_c(self):
        return self.value[30]

    def set_b(self, flag):
        self.value[31] = flag

    def get_b(self):
        return self.value[31]


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
