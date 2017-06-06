from armulator.all_registers.abstract_register import AbstractRegister


class FCSEIDR(AbstractRegister):
    """
    FCSE Process ID Register
    """

    def __init__(self):
        super(FCSEIDR, self).__init__()

    def set_pid(self, pid):
        self.value[0:7] = pid

    def get_pid(self):
        return self.value[0:7]
