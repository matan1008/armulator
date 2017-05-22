from bitstring import BitArray


class SCR(object):
    """
    Secure Configuration Register
    """

    def __init__(self):
        self.value = BitArray(length=32)

    def set_ns(self, flag):
        self.value[31] = flag

    def get_ns(self):
        return self.value[31]

    def set_irq(self, flag):
        self.value[30] = flag

    def get_irq(self):
        return self.value[30]

    def set_fiq(self, flag):
        self.value[29] = flag

    def get_fiq(self):
        return self.value[29]

    def set_ea(self, flag):
        self.value[28] = flag

    def get_ea(self):
        return self.value[28]

    def set_fw(self, flag):
        self.value[27] = flag

    def get_fw(self):
        return self.value[27]

    def set_aw(self, flag):
        self.value[26] = flag

    def get_aw(self):
        return self.value[26]

    def set_net(self, flag):
        self.value[25] = flag

    def get_net(self):
        return self.value[25]

    def set_scd(self, flag):
        self.value[24] = flag

    def get_scd(self):
        return self.value[24]

    def set_hce(self, flag):
        self.value[23] = flag

    def get_hce(self):
        return self.value[23]

    def set_sif(self, flag):
        self.value[22] = flag

    def get_sif(self):
        return self.value[22]
