from armulator.all_registers.abstract_register import AbstractRegister


class DBGDIDR(AbstractRegister):
    """
    Debug ID Register
    """

    def __init__(self):
        super(DBGDIDR, self).__init__()

    def set_wrps(self, wrps):
        self.value[0:4] = wrps

    def get_wrps(self):
        return self.value[0:4]

    def set_brps(self, brps):
        self.value[4:8] = brps

    def get_brps(self):
        return self.value[4:8]

    def set_ctx_cmps(self, ctx_cmps):
        self.value[8:12] = ctx_cmps

    def get_ctx_cmps(self):
        return self.value[8:12]

    def set_version(self, version):
        self.value[12:16] = version

    def get_version(self):
        return self.value[12:16]

    def set_devid_imp(self, flag):
        self.value[16] = flag

    def get_devid_imp(self):
        return self.value[16]

    def set_nsuhd_imp(self, flag):
        self.value[17] = flag

    def get_nsuhd_imp(self):
        return self.value[17]

    def set_pcsr_imp(self, flag):
        self.value[18] = flag

    def get_pcsr_imp(self):
        return self.value[18]

    def set_se_imp(self, flag):
        self.value[19] = flag

    def get_se_imp(self):
        return self.value[19]

    def set_variant(self, variant):
        self.value[24:28] = variant

    def get_variant(self):
        return self.value[24:28]

    def set_revision(self, revision):
        self.value[28:32] = revision

    def get_revision(self):
        return self.value[28:32]
