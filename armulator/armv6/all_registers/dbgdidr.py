from armulator.armv6.all_registers.abstract_register import AbstractRegister


class DBGDIDR(AbstractRegister):
    """
    Debug ID Register
    """

    @property
    def wrps(self):
        return self[31:28]

    @wrps.setter
    def wrps(self, wrps):
        self[31:28] = wrps

    @property
    def brps(self):
        return self[27:24]

    @brps.setter
    def brps(self, brps):
        self[27:24] = brps

    @property
    def ctx_cmps(self):
        return self[23:20]

    @ctx_cmps.setter
    def ctx_cmps(self, ctx_cmps):
        self[23:20] = ctx_cmps

    @property
    def version(self):
        return self[19:16]

    @version.setter
    def version(self, version):
        self[19:16] = version

    @property
    def devid_imp(self):
        return self[15]

    @devid_imp.setter
    def devid_imp(self, flag):
        self[15] = flag

    @property
    def nsuhd_imp(self):
        return self[14]

    @nsuhd_imp.setter
    def nsuhd_imp(self, flag):
        self[14] = flag

    @property
    def pcsr_imp(self):
        return self[13]

    @pcsr_imp.setter
    def pcsr_imp(self, flag):
        self[13] = flag

    @property
    def se_imp(self):
        return self[12]

    @se_imp.setter
    def se_imp(self, flag):
        self[12] = flag

    @property
    def variant(self):
        return self[7:4]

    @variant.setter
    def variant(self, variant):
        self[7:4] = variant

    @property
    def revision(self):
        return self[3:0]

    @revision.setter
    def revision(self, revision):
        self[3:0] = revision
