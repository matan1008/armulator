from armulator.all_registers.abstract_register import AbstractRegister


class SUNAVCR(AbstractRegister):
    """
    Secure User and non-secure Access Validation Control Register
    """

    def __init__(self):
        super(SUNAVCR, self).__init__()

    def set_v(self, flag):
        self.value[31] = flag

    def get_v(self):
        return self.value[31]
