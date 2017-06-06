from armulator.all_registers.abstract_register import AbstractRegister


class HSR(AbstractRegister):
    """
    Hyp Syndrome Register
    """

    def __init__(self):
        super(HSR, self).__init__()

    def set_ec(self, ec):
        self.value[0:6] = ec

    def get_ec(self):
        return self.value[0:6]

    def set_il(self, flag):
        self.value[6] = flag

    def get_il(self):
        return self.value[6]

    def set_iss(self, iss):
        self.value[7:32] = iss

    def get_iss(self):
        return self.value[7:32]
