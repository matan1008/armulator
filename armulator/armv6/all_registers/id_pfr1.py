from armulator.armv6.all_registers.abstract_register import AbstractRegister


class IdPfr1(AbstractRegister):
    """
    Processor Feature Register 1
    """

    @property
    def gt(self):
        """
        Generic Timer Extension
        """
        return self[19:16]

    @gt.setter
    def gt(self, gt):
        """
        Generic Timer Extension
        :param gt:
        """
        self[19:16] = gt

    @property
    def ve(self):
        """
        Virtualization Extensions
        """
        return self[15:12]

    @ve.setter
    def ve(self, ve):
        """
        Virtualization Extensions
        :param ve:
        """
        self[15:12] = ve

    @property
    def m_profile(self):
        """
        M profile programmers' model
        """
        return self[11:8]

    @m_profile.setter
    def m_profile(self, m_profile):
        """
        M profile programmers' model
        :param m_profile:
        """
        self[11:8] = m_profile

    @property
    def se(self):
        """
        Security Extensions
        """
        return self[7:4]

    @se.setter
    def se(self, se):
        """
        Security Extensions
        :param se:
        """
        self[7:4] = se

    @property
    def pm(self):
        """
        Programmers' model
        """
        return self[3:0]

    @pm.setter
    def pm(self, pm):
        """
        Programmers' model
        :param pm:
        """
        self[3:0] = pm
