from armulator.armv6.all_registers.abstract_register import AbstractRegister


class RSR(AbstractRegister):
    """
    Region Size and Enable Register
    """

    def get_sd_n(self, n):
        return self[8 + n]

    def set_sd_n(self, n, flag):
        self[8 + n] = flag

    @property
    def rsize(self):
        return self[5:1]

    @rsize.setter
    def rsize(self, rsize):
        self[5:1] = rsize

    @property
    def en(self):
        return self[0]

    @en.setter
    def en(self, flag):
        self[0] = flag


class DRSR(RSR):
    """
    Data Region Size and Enable Register
    """
    pass


class IRSR(RSR):
    """
    Instruction Region Size and Enable Register
    """
    pass
