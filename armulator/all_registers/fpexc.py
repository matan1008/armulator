from armulator.all_registers.abstract_register import AbstractRegister


class FPEXC(AbstractRegister):
    """
    Floating-Point Exception Control register
    """

    def __init__(self):
        super(FPEXC, self).__init__()

    def set_ex(self, flag):
        self.value[0] = flag

    def get_ex(self):
        return self.value[0]

    def set_en(self, flag):
        self.value[0] = flag

    def get_en(self):
        return self.value[0]
