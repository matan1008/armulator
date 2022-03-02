from armulator.armv6.all_registers.abstract_register import AbstractRegister


class RGNR(AbstractRegister):
    """
    MPU Region Number Register
    """

    def __init__(self, number_of_regions):
        super(RGNR, self).__init__()
        self.n = number_of_regions.bit_length()

    def set_region(self, region):
        self[self.n - 1:0] = region

    def get_region(self):
        return self[self.n - 1:0]
