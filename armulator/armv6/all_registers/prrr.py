from armulator.armv6.all_registers.abstract_register import AbstractRegister


class PRRR(AbstractRegister):
    """
    Primary Region Remap Register
    """

    def __init__(self):
        super(PRRR, self).__init__()

    def set_tr_n(self, n, tr):
        self.value[30 - (2 * n):32 - (2 * n)] = tr

    def get_tr_n(self, n):
        return self.value[30 - (2 * n):32 - (2 * n)]

    def set_nos_n(self, n, flag):
        self.value[7 - n] = flag

    def get_nos_n(self, n):
        return self.value[7 - n]

    def set_ns1(self, flag):
        self.value[12] = flag

    def get_ns1(self):
        return self.value[12]

    def set_ns0(self, flag):
        self.value[13] = flag

    def get_ns0(self):
        return self.value[13]

    def set_ds1(self, flag):
        self.value[14] = flag

    def get_ds1(self):
        return self.value[14]

    def set_ds0(self, flag):
        self.value[15] = flag

    def get_ds0(self):
        return self.value[15]
