from armulator.armv6.all_registers.abstract_register import AbstractRegister


class HCPTR(AbstractRegister):
    """
    Hyp Coprocessor Trap Register
    """

    @property
    def tcpac(self):
        return self[31]

    @tcpac.setter
    def tcpac(self, flag):
        self[31] = flag

    @property
    def tta(self):
        return self[20]

    @tta.setter
    def tta(self, flag):
        self[20] = flag

    @property
    def tase(self):
        return self[15]

    @tase.setter
    def tase(self, flag):
        self[15] = flag

    def get_tcp_n(self, n):
        return self[n]

    def set_tcp_n(self, n, flag):
        self[n] = flag
