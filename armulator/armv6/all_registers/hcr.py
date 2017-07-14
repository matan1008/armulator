from armulator.armv6.all_registers.abstract_register import AbstractRegister


class HCR(AbstractRegister):
    """
    Hyp Configuration Register
    """

    def __init__(self):
        super(HCR, self).__init__()

    def set_tge(self, flag):
        self.value[4] = flag

    def get_tge(self):
        return self.value[4]

    def set_tvm(self, flag):
        self.value[5] = flag

    def get_tvm(self):
        return self.value[5]

    def set_ttlb(self, flag):
        self.value[6] = flag

    def get_ttlb(self):
        return self.value[6]

    def set_tpu(self, flag):
        self.value[7] = flag

    def get_tpu(self):
        return self.value[7]

    def set_tpc(self, flag):
        self.value[8] = flag

    def get_tpc(self):
        return self.value[8]

    def set_tsw(self, flag):
        self.value[9] = flag

    def get_tsw(self):
        return self.value[9]

    def set_tac(self, flag):
        self.value[10] = flag

    def get_tac(self):
        return self.value[10]

    def set_tidcp(self, flag):
        self.value[11] = flag

    def get_tidcp(self):
        return self.value[11]

    def set_tsc(self, flag):
        self.value[12] = flag

    def get_tsc(self):
        return self.value[12]

    def set_tid_n(self, n, flag):
        assert 0 <= n < 4
        self.value[16 - n] = flag

    def get_tid_n(self, n):
        assert 0 <= n < 4
        return self.value[16 - n]

    def set_twe(self, flag):
        self.value[17] = flag

    def get_twe(self):
        return self.value[17]

    def set_twi(self, flag):
        self.value[18] = flag

    def get_twi(self):
        return self.value[18]

    def set_dc(self, flag):
        self.value[19] = flag

    def get_dc(self):
        return self.value[19]

    def set_bsu(self, bsu):
        self.value[20:22] = bsu

    def get_bsu(self):
        return self.value[20:22]

    def set_fb(self, flag):
        self.value[22] = flag

    def get_fb(self):
        return self.value[22]

    def set_va(self, flag):
        self.value[23] = flag

    def get_va(self):
        return self.value[23]

    def set_vi(self, flag):
        self.value[24] = flag

    def get_vi(self):
        return self.value[24]

    def set_vf(self, flag):
        self.value[25] = flag

    def get_vf(self):
        return self.value[25]

    def set_amo(self, flag):
        self.value[26] = flag

    def get_amo(self):
        return self.value[26]

    def set_imo(self, flag):
        self.value[27] = flag

    def get_imo(self):
        return self.value[27]

    def set_fmo(self, flag):
        self.value[28] = flag

    def get_fmo(self):
        return self.value[28]

    def set_ptw(self, flag):
        self.value[29] = flag

    def get_ptw(self):
        return self.value[29]

    def set_swio(self, flag):
        self.value[30] = flag

    def get_swio(self):
        return self.value[30]

    def set_vm(self, flag):
        self.value[31] = flag

    def get_vm(self):
        return self.value[31]
