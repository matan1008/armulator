from armulator.armv6.all_registers.abstract_register import AbstractRegister


class HCR(AbstractRegister):
    """
    Hyp Configuration Register
    """

    @property
    def tge(self):
        return self[27]

    @tge.setter
    def tge(self, flag):
        self[27] = flag

    @property
    def tvm(self):
        return self[26]

    @tvm.setter
    def tvm(self, flag):
        self[26] = flag

    @property
    def ttlb(self):
        return self[25]

    @ttlb.setter
    def ttlb(self, flag):
        self[25] = flag

    @property
    def tpu(self):
        return self[24]

    @tpu.setter
    def tpu(self, flag):
        self[24] = flag

    @property
    def tpc(self):
        return self[23]

    @tpc.setter
    def tpc(self, flag):
        self[23] = flag

    @property
    def tsw(self):
        return self[22]

    @tsw.setter
    def tsw(self, flag):
        self[22] = flag

    @property
    def tac(self):
        return self[21]

    @tac.setter
    def tac(self, flag):
        self[21] = flag

    @property
    def tidcp(self):
        return self[20]

    @tidcp.setter
    def tidcp(self, flag):
        self[20] = flag

    @property
    def tsc(self):
        return self[19]

    @tsc.setter
    def tsc(self, flag):
        self[19] = flag

    def set_tid_n(self, n, flag):
        assert 0 <= n < 4
        self[15 + n] = flag

    def get_tid_n(self, n):
        assert 0 <= n < 4
        return self[15 + n]

    @property
    def twe(self):
        return self[14]

    @twe.setter
    def twe(self, flag):
        self[14] = flag

    @property
    def twi(self):
        return self[13]

    @twi.setter
    def twi(self, flag):
        self[13] = flag

    @property
    def dc(self):
        return self[12]

    @dc.setter
    def dc(self, flag):
        self[12] = flag

    @property
    def bsu(self):
        return self[11:10]

    @bsu.setter
    def bsu(self, bsu):
        self[11:10] = bsu

    @property
    def fb(self):
        return self[9]

    @fb.setter
    def fb(self, flag):
        self[9] = flag

    @property
    def va(self):
        return self[8]

    @va.setter
    def va(self, flag):
        self[8] = flag

    @property
    def vi(self):
        return self[7]

    @vi.setter
    def vi(self, flag):
        self[7] = flag

    @property
    def vf(self):
        return self[6]

    @vf.setter
    def vf(self, flag):
        self[6] = flag

    @property
    def amo(self):
        return self[5]

    @amo.setter
    def amo(self, flag):
        self[5] = flag

    @property
    def imo(self):
        return self[4]

    @imo.setter
    def imo(self, flag):
        self[4] = flag

    @property
    def fmo(self):
        return self[3]

    @fmo.setter
    def fmo(self, flag):
        self[3] = flag

    @property
    def ptw(self):
        return self[2]

    @ptw.setter
    def ptw(self, flag):
        self[2] = flag

    @property
    def swio(self):
        return self[1]

    @swio.setter
    def swio(self, flag):
        self[1] = flag

    @property
    def vm(self):
        return self[0]

    @vm.setter
    def vm(self, flag):
        self[0] = flag
