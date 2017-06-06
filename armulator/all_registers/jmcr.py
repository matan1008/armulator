from armulator.all_registers.abstract_register import AbstractRegister


class JMCR(AbstractRegister):
    """
    Jazelle Main Configuration Register
    """

    def __init__(self):
        super(JMCR, self).__init__()

    def set_je(self, flag):
        self.value[31] = flag

    def get_je(self):
        return self.value[31]
