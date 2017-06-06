from armulator.all_registers.abstract_register import AbstractRegister


class HSCTLR(AbstractRegister):
    """
    Hyp System Control Register
    """

    def __init__(self):
        super(HSCTLR, self).__init__()

    def set_te(self, flag):
        self.value[1] = flag

    def get_te(self):
        return self.value[1]

    def set_ee(self, flag):
        self.value[6] = flag

    def get_ee(self):
        return self.value[6]

    def set_fi(self, flag):
        self.value[10] = flag

    def get_fi(self):
        return self.value[10]

    def set_wxn(self, flag):
        self.value[12] = flag

    def get_wxn(self):
        return self.value[12]

    def set_i(self, flag):
        self.value[19] = flag

    def get_i(self):
        return self.value[19]

    def set_cp15ben(self, flag):
        self.value[26] = flag

    def get_cp15ben(self):
        return self.value[26]

    def set_c(self, flag):
        self.value[29] = flag

    def get_c(self):
        return self.value[29]

    def set_a(self, flag):
        self.value[30] = flag

    def get_a(self):
        return self.value[30]

    def set_m(self, flag):
        self.value[31] = flag

    def get_m(self):
        return self.value[31]
