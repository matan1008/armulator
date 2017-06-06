from armulator.all_registers.abstract_register import AbstractRegister


class MIDR(AbstractRegister):
    """
    Main ID Register
    """

    def __init__(self):
        super(MIDR, self).__init__()

    def set_implementer(self, implementer):
        self.value[0:8] = implementer

    def get_implementer(self):
        return self.value[0:8]

    def set_variant(self, variant):
        self.value[8:12] = variant

    def get_variant(self):
        return self.value[8:12]

    def set_architecture(self, architecture):
        self.value[12:16] = architecture

    def get_architecture(self):
        return self.value[12:16]

    def set_primary_part_number(self, number):
        self.value[16:28] = number

    def get_primary_part_number(self):
        return self.value[16:28]

    def set_revision(self, revision):
        self.value[28:32] = revision

    def get_revision(self):
        return self.value[28:32]
