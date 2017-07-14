from armulator.armv6.all_registers.abstract_register import AbstractRegister


class IdPfr1(AbstractRegister):
    """
    Processor Feature Register 1
    """

    def __init__(self):
        super(IdPfr1, self).__init__()

    def set_gt(self, gt):
        """
        Generic Timer Extension
        :param gt:
        """
        self.value[12:16] = gt

    def get_gt(self):
        """
        Generic Timer Extension
        """
        return self.value[12:16]

    def set_ve(self, ve):
        """
        Virtualization Extensions
        :param ve:
        """
        self.value[16:20] = ve

    def get_ve(self):
        """
        Virtualization Extensions
        """
        return self.value[16:20]

    def set_m_profile(self, m_profile):
        """
        M profile programmers' model
        :param m_profile:
        """
        self.value[20:24] = m_profile

    def get_m_profile(self):
        """
        M profile programmers' model
        """
        return self.value[20:24]

    def set_se(self, se):
        """
        Security Extensions
        :param se:
        """
        self.value[24:28] = se

    def get_se(self):
        """
        Security Extensions
        """
        return self.value[24:28]

    def set_pm(self, pm):
        """
        Programmers' model
        :param pm:
        """
        self.value[28:32] = pm

    def get_pm(self):
        """
        Programmers' model
        """
        return self.value[28:32]
