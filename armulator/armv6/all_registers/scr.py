from armulator.armv6.all_registers.abstract_register import AbstractRegister


class SCR(AbstractRegister):
    """
    Secure Configuration Register
    """

    @property
    def ns(self):
        return self[0]

    @ns.setter
    def ns(self, flag):
        self[0] = flag

    @property
    def irq(self):
        return self[1]

    @irq.setter
    def irq(self, flag):
        self[1] = flag

    @property
    def fiq(self):
        return self[2]

    @fiq.setter
    def fiq(self, flag):
        self[2] = flag

    @property
    def ea(self):
        return self[3]

    @ea.setter
    def ea(self, flag):
        self[3] = flag

    @property
    def fw(self):
        return self[4]

    @fw.setter
    def fw(self, flag):
        self[4] = flag

    @property
    def aw(self):
        return self[5]

    @aw.setter
    def aw(self, flag):
        self[5] = flag

    @property
    def net(self):
        return self[6]

    @net.setter
    def net(self, flag):
        self[6] = flag

    @property
    def scd(self):
        return self[7]

    @scd.setter
    def scd(self, flag):
        self[7] = flag

    @property
    def hce(self):
        return self[8]

    @hce.setter
    def hce(self, flag):
        self[8] = flag

    @property
    def sif(self):
        return self[9]

    @sif.setter
    def sif(self, flag):
        self[9] = flag
