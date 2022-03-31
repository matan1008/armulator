from armulator.armv6.all_registers.abstract_register import AbstractRegister


class HSR(AbstractRegister):
    """
    Hyp Syndrome Register
    """

    @property
    def ec(self):
        return self[31:26]

    @ec.setter
    def ec(self, ec):
        self[31:26] = ec

    @property
    def il(self):
        return self[25]

    @il.setter
    def il(self, flag):
        self[25] = flag

    @property
    def iss(self):
        return self[24:0]

    @iss.setter
    def iss(self, iss):
        self[24:0] = iss
