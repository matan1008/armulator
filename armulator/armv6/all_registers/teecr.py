from armulator.armv6.all_registers.abstract_register import AbstractRegister


class TEECR(AbstractRegister):
    """
    ThumbEE Configuration Register
    """

    @property
    def xed(self):
        return self[0]

    @xed.setter
    def xed(self, flag):
        self[0] = flag
