from armulator.armv6.all_registers.abstract_register import AbstractRegister


class HDCR(AbstractRegister):
    """
    Hyp Debug Configuration Register
    """

    @property
    def tdra(self):
        return self[11]

    @tdra.setter
    def tdra(self, flag):
        self[11] = flag

    @property
    def tdosa(self):
        return self[10]

    @tdosa.setter
    def tdosa(self, flag):
        self[10] = flag

    @property
    def tda(self):
        return self[9]

    @tda.setter
    def tda(self, flag):
        self[9] = flag

    @property
    def tde(self):
        return self[8]

    @tde.setter
    def tde(self, flag):
        self[8] = flag

    @property
    def hpme(self):
        return self[7]

    @hpme.setter
    def hpme(self, flag):
        self[7] = flag

    @property
    def tpm(self):
        return self[6]

    @tpm.setter
    def tpm(self, flag):
        self[6] = flag

    @property
    def tpmcr(self):
        return self[5]

    @tpmcr.setter
    def tpmcr(self, flag):
        self[5] = flag

    @property
    def hpmn(self):
        return self[4:0]

    @hpmn.setter
    def hpmn(self, hpmn):
        self[4:0] = hpmn
