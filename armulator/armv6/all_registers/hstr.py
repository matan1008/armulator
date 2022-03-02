from armulator.armv6.all_registers.abstract_register import AbstractRegister


class HSTR(AbstractRegister):
    """
    Hyp System Trap Register
    """

    @property
    def tjdbx(self):
        return self[17]

    @tjdbx.setter
    def tjdbx(self, flag):
        self[17] = flag

    @property
    def ttee(self):
        return self[16]

    @ttee.setter
    def ttee(self, flag):
        self[16] = flag

    def get_t_n(self, n):
        return self[n]

    def set_t_n(self, n, flag):
        self[n] = flag
