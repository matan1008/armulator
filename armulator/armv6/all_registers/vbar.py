from armulator.armv6.all_registers.abstract_register import AbstractRegister


class VBAR(AbstractRegister):
    """
    Vector Base Address Register
    """

    def __init__(self):
        super(VBAR, self).__init__()

    def set_base_address(self, base_address):
        self.value[0:27] = base_address

    def get_base_address(self):
        return self.value[0:27]
