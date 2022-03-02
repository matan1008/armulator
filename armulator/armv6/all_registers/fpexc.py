from armulator.armv6.all_registers.abstract_register import AbstractRegister


class FPEXC(AbstractRegister):
    """
    Floating-Point Exception Control register
    """

    @property
    def ex(self):
        return self[31]

    @ex.setter
    def ex(self, flag):
        self[31] = flag

    @property
    def en(self):
        return self[30]

    @en.setter
    def en(self, flag):
        self[30] = flag
