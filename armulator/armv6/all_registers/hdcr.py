from armulator.armv6.all_registers.abstract_register import AbstractRegister


class HDCR(AbstractRegister):
    """
    Hyp Debug Configuration Register
    """

    def __init__(self):
        super(HDCR, self).__init__()

    def set_tdra(self, flag):
        self.value[20] = flag

    def get_tdra(self):
        return self.value[20]

    def set_tdosa(self, flag):
        self.value[21] = flag

    def get_tdosa(self):
        return self.value[21]

    def set_tda(self, flag):
        self.value[22] = flag

    def get_tda(self):
        return self.value[22]

    def set_tde(self, flag):
        self.value[23] = flag

    def get_tde(self):
        return self.value[23]

    def set_hpme(self, flag):
        self.value[24] = flag

    def get_hpme(self):
        return self.value[24]

    def set_tpm(self, flag):
        self.value[25] = flag

    def get_tpm(self):
        return self.value[25]

    def set_tpmcr(self, flag):
        self.value[26] = flag

    def get_tpmcr(self):
        return self.value[26]

    def set_hpmn(self, hpmn):
        self.value[27:32] = hpmn

    def get_hpmn(self):
        return self.value[27:32]
