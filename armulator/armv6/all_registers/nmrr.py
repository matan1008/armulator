from armulator.armv6.all_registers.abstract_register import AbstractRegister


class NMRR(AbstractRegister):
    """
    Normal Memory Remap Register
    """

    def get_ir_n(self, n):
        assert n < 8
        return self[(2 * n) + 1:2 * n]

    def set_ir_n(self, n, ir):
        assert n < 8
        self[(2 * n) + 1:2 * n] = ir

    def get_or_n(self, n):
        assert n < 8
        return self[(2 * n) + 17:(2 * n) + 16]

    def set_or_n(self, n, or_):
        assert n < 8
        self[(2 * n) + 17:(2 * n) + 16] = or_
