from armulator.armv6.all_registers.abstract_register import AbstractRegister


class JMCR(AbstractRegister):
    """
    Jazelle Main Configuration Register
    """

    @property
    def je(self):
        return self[0]

    @je.setter
    def je(self, flag):
        self[0] = flag
