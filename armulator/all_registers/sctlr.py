from armulator.all_registers.abstract_register import AbstractRegister


class SCTLR(AbstractRegister):
    """
    System Control Register
    """

    def __init__(self):
        super(SCTLR, self).__init__()

    def set_ie(self, flag):
        self.value[0] = flag

    def get_ie(self):
        return self.value[0]

    def set_te(self, flag):
        self.value[1] = flag

    def get_te(self):
        return self.value[1]

    def set_afe(self, flag):
        self.value[2] = flag

    def get_afe(self):
        return self.value[2]

    def set_tre(self, flag):
        self.value[3] = flag

    def get_tre(self):
        return self.value[3]

    def set_nmfi(self, flag):
        self.value[4] = flag

    def get_nmfi(self):
        return self.value[4]

    def set_ee(self, flag):
        self.value[6] = flag

    def get_ee(self):
        return self.value[6]

    def set_ve(self, flag):
        self.value[7] = flag

    def get_ve(self):
        return self.value[7]

    def set_u(self, flag):
        self.value[9] = flag

    def get_u(self):
        return self.value[9]

    def set_fi(self, flag):
        self.value[10] = flag

    def get_fi(self):
        return self.value[10]

    def set_uwxn(self, flag):
        self.value[11] = flag

    def get_uwxn(self):
        return self.value[11]

    def set_wxn(self, flag):
        self.value[12] = flag

    def get_wxn(self):
        return self.value[12]

    def set_dz(self, flag):
        self.value[12] = flag

    def get_dz(self):
        return self.value[12]

    def set_ha(self, flag):
        self.value[14] = flag

    def get_ha(self):
        return self.value[14]

    def set_br(self, flag):
        self.value[14] = flag

    def get_br(self):
        return self.value[14]

    def set_rr(self, flag):
        self.value[17] = flag

    def get_rr(self):
        return self.value[17]

    def set_v(self, flag):
        self.value[18] = flag

    def get_v(self):
        return self.value[18]

    def set_i(self, flag):
        self.value[19] = flag

    def get_i(self):
        return self.value[19]

    def set_z(self, flag):
        self.value[20] = flag

    def get_z(self):
        return self.value[20]

    def set_sw(self, flag):
        self.value[21] = flag

    def get_sw(self):
        return self.value[21]

    def set_b(self, flag):
        self.value[24] = flag

    def get_b(self):
        return self.value[24]

    def set_cp15ben(self, flag):
        self.value[26] = flag

    def get_cp15ben(self):
        return self.value[26]

    def set_c(self, flag):
        self.value[29] = flag

    def get_c(self):
        return self.value[29]

    def set_a(self, flag):
        self.value[30] = flag

    def get_a(self):
        return self.value[30]

    def set_m(self, flag):
        self.value[31] = flag

    def get_m(self):
        return self.value[31]
