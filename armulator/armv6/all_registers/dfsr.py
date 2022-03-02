from armulator.armv6.all_registers.abstract_register import AbstractRegister
from armulator.armv6.bits_ops import chain, bit_at, substring


class DFSR(AbstractRegister):
    """
    Data Fault Status Register
    """

    @property
    def cm(self):
        return self[13]

    @cm.setter
    def cm(self, flag):
        self[13] = flag

    @property
    def ext(self):
        return self[12]

    @ext.setter
    def ext(self, flag):
        self[12] = flag

    @property
    def wnr(self):
        return self[11]

    @wnr.setter
    def wnr(self, flag):
        self[11] = flag

    @property
    def fs(self):
        return chain(self[10], self[3:0], 4)

    @fs.setter
    def fs(self, fs):
        self[10] = bit_at(fs, 4)
        self[3:0] = substring(fs, 3, 0)

    @property
    def lpae(self):
        return self[9]

    @lpae.setter
    def lpae(self, flag):
        self[9] = flag

    @property
    def domain(self):
        return self[7:4]

    @domain.setter
    def domain(self, domain):
        self[7:4] = domain

    @property
    def status(self):
        return self[5:0]

    @status.setter
    def status(self, status):
        self[5:0] = status
