from armulator.armv6.all_registers.abstract_register import AbstractRegister


class CPACR(AbstractRegister):
    """
    Coprocessor Access Control Register
    """

    def get_cp_n(self, n):
        assert n < 14
        return self[1 + (2 * n): 2 * n]

    def set_cp_n(self, n, cp):
        assert n < 14
        self[1 + (2 * n):2 * n] = cp

    @property
    def trcdis(self):
        return self[28]

    @trcdis.setter
    def trcdis(self, flag):
        self[28] = flag

    @property
    def d32dis(self):
        return self[30]

    @d32dis.setter
    def d32dis(self, flag):
        self[30] = flag

    @property
    def asedis(self):
        return self[31]

    @asedis.setter
    def asedis(self, flag):
        self[31] = flag
