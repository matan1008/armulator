from armulator.armv6.all_registers.abstract_register import AbstractRegister


class TEECR(AbstractRegister):
    """
    ThumbEE Configuration Register
    """

    def __init__(self):
        super(TEECR, self).__init__()

    def set_xed(self, flag):
        self.value[31] = flag

    def get_xed(self):
        return self.value[31]
