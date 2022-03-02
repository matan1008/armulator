from armulator.armv6.all_registers.abstract_register import AbstractRegister


class SUNAVCR(AbstractRegister):
    """
    Secure User and non-secure Access Validation Control Register
    """

    @property
    def v(self):
        return self[0]

    @v.setter
    def v(self, flag):
        self[0] = flag
