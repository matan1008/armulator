from armulator.armv6.all_registers.abstract_register import AbstractRegister


class MPUIR(AbstractRegister):
    """
    MPU Type Register
    """

    @property
    def nu(self):
        return self[0]

    @nu.setter
    def nu(self, flag):
        self[0] = flag

    @property
    def iregion(self):
        return self[23:16]

    @iregion.setter
    def iregion(self, iregion):
        self[23:16] = iregion

    @property
    def dregion(self):
        return self[15:8]

    @dregion.setter
    def dregion(self, dregion):
        self[15:8] = dregion
