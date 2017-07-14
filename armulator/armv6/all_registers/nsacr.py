from armulator.armv6.all_registers.abstract_register import AbstractRegister


class NSACR(AbstractRegister):
    """
    Non-Secure Access Control Register
    """

    def __init__(self):
        super(NSACR, self).__init__()

    def set_cp_n(self, n, flag):
        assert n < 14
        self.value[31 - n] = flag

    def get_cp_n(self, n):
        assert n < 14
        return self.value[31 - n]

    def set_nsd32dis(self, flag):
        self.value[17] = flag

    def get_nsd32dis(self):
        return self.value[17]

    def set_nsasedis(self, flag):
        self.value[16] = flag

    def get_nsasedis(self):
        return self.value[16]

    def set_rfr(self, flag):
        self.value[12] = flag

    def get_rfr(self):
        return self.value[12]

    def set_nstrcdis(self, flag):
        self.value[11] = flag

    def get_nstrcdis(self):
        return self.value[11]
