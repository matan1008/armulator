from armulator.armv6.all_registers.abstract_register import AbstractRegister


class HPFAR(AbstractRegister):
    """
    Hyp IPA Fault Address Register
    """

    @property
    def fipa(self):
        return self[31:4]

    @fipa.setter
    def fipa(self, fipa):
        self[31:4] = fipa
