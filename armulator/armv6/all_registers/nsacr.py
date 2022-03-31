from armulator.armv6.all_registers.abstract_register import AbstractRegister


class NSACR(AbstractRegister):
    """
    Non-Secure Access Control Register
    """

    def set_cp_n(self, n, flag):
        assert n < 14
        self[n] = flag

    def get_cp_n(self, n):
        assert n < 14
        return self[n]

    @property
    def nsd32dis(self):
        return self[14]

    @nsd32dis.setter
    def nsd32dis(self, flag):
        self[14] = flag

    @property
    def nsasedis(self):
        return self[15]

    @nsasedis.setter
    def nsasedis(self, flag):
        self[15] = flag

    @property
    def rfr(self):
        return self[19]

    @rfr.setter
    def rfr(self, flag):
        self[19] = flag

    @property
    def nstrcdis(self):
        return self[20]

    @nstrcdis.setter
    def nstrcdis(self, flag):
        self[20] = flag
