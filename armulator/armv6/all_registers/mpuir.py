from armulator.armv6.all_registers.abstract_register import AbstractRegister


class MPUIR(AbstractRegister):
    """
    MPU Type Register
    """

    def __init__(self):
        super(MPUIR, self).__init__()

    def set_nu(self, flag):
        self.value[31] = flag

    def get_nu(self):
        return self.value[31]

    def set_iregion(self, iregion):
        self.value[8:16] = iregion

    def get_iregion(self):
        return self.value[8:16]

    def set_dregion(self, dregion):
        self.value[16:24] = dregion

    def get_dregion(self):
        return self.value[16:24]
