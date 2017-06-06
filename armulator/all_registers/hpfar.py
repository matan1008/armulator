from armulator.all_registers.abstract_register import AbstractRegister


class HPFAR(AbstractRegister):
    """
    Hyp IPA Fault Address Register
    """

    def __init__(self):
        super(HPFAR, self).__init__()

    def set_fipa(self, fipa):
        self.value[0:28] = fipa

    def get_fipa(self):
        return self.value[0:28]
