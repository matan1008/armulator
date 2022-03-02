from armulator.armv6.all_registers.abstract_register import AbstractRegister


class DACR(AbstractRegister):
    """
    Domain Access Control Register
    """

    def get_d_n(self, n):
        assert n < 16
        return self[(2 * n) + 1:2 * n]

    def set_d_n(self, n, d):
        assert n < 16
        self[(2 * n) + 1:2 * n] = d
