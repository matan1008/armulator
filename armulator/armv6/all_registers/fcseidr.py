from armulator.armv6.all_registers.abstract_register import AbstractRegister


class FCSEIDR(AbstractRegister):
    """
    FCSE Process ID Register
    """

    @property
    def pid(self):
        return self[31:25]

    @pid.setter
    def pid(self, pid):
        self[31:25] = pid
