from armulator.all_registers.abstract_register import AbstractRegister


class HSTR(AbstractRegister):
    """
    Hyp System Trap Register
    """

    def __init__(self):
        super(HSTR, self).__init__()

    def set_tjdbx(self, flag):
        self.value[14] = flag

    def get_tjdbx(self):
        return self.value[14]

    def set_ttee(self, flag):
        self.value[15] = flag

    def get_ttee(self):
        return self.value[15]

    def set_t_n(self, n, flag):
        self.value[31 - n] = flag

    def get_t_n(self, n):
        return self.value[31 - n]
