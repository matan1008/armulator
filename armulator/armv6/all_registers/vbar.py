from armulator.armv6.all_registers.abstract_register import AbstractRegister


class VBAR(AbstractRegister):
    """
    Vector Base Address Register
    """

    def set_base_address(self, base_address):
        self[31:5] = base_address

    def get_base_address(self):
        return self[31:5]
