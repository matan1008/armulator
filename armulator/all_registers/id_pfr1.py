from bitstring import BitArray


class IdPfr1(object):
    """
    Processor Feature Register 1
    """

    def __init__(self):
        self.value = BitArray(length=32)

    def set_gt(self, gt):
        """
        Generic Timer Extension
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
        """
        self.value[28:32] = pm

    def get_pm(self):
        """
        Programmers' model
        """
        return self.value[28:32]
