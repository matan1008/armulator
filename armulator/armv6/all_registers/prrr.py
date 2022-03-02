from armulator.armv6.all_registers.abstract_register import AbstractRegister


class PRRR(AbstractRegister):
    """
    Primary Region Remap Register
    """

    def get_tr_n(self, n):
        return self[(2 * n) + 1:2 * n]

    def set_tr_n(self, n, tr):
        self[(2 * n) + 1:2 * n] = tr

    def get_nos_n(self, n):
        return self[n + 24]

    def set_nos_n(self, n, flag):
        self[n + 24] = flag

    @property
    def ns1(self):
        return self[19]

    @ns1.setter
    def ns1(self, flag):
        self[19] = flag

    @property
    def ns0(self):
        return self[18]

    @ns0.setter
    def ns0(self, flag):
        self[18] = flag

    @property
    def ds1(self):
        return self[17]

    @ds1.setter
    def ds1(self, flag):
        self[17] = flag

    @property
    def ds0(self):
        return self[16]

    @ds0.setter
    def ds0(self, flag):
        self[16] = flag
