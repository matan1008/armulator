from armulator.armv6.all_registers.abstract_register import AbstractRegister


class SDER(AbstractRegister):
    """
    Secure Debug Enable Register
    """

    @property
    def suniden(self):
        return self[1]

    @suniden.setter
    def suniden(self, flag):
        self[1] = flag

    @property
    def suiden(self):
        return self[0]

    @suiden.setter
    def suiden(self, flag):
        self[0] = flag
