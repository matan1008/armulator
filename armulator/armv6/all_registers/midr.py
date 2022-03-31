from armulator.armv6.all_registers.abstract_register import AbstractRegister


class MIDR(AbstractRegister):
    """
    Main ID Register
    """

    @property
    def implementer(self):
        return self[31:24]

    @implementer.setter
    def implementer(self, implementer):
        self[31:24] = implementer

    @property
    def variant(self):
        return self[23:20]

    @variant.setter
    def variant(self, variant):
        self[23:20] = variant

    @property
    def architecture(self):
        return self[19:16]

    @architecture.setter
    def architecture(self, architecture):
        self[19:16] = architecture

    @property
    def primary_part_number(self):
        return self[15:4]

    @primary_part_number.setter
    def primary_part_number(self, number):
        self[15:4] = number

    @property
    def revision(self):
        return self[3:0]

    @revision.setter
    def revision(self, revision):
        self[3:0] = revision
