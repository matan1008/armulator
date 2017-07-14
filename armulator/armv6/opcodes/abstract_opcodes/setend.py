from armulator.armv6.opcodes.abstract_opcode import AbstractOpcode


class Setend(AbstractOpcode):
    def __init__(self, set_bigend):
        super(Setend, self).__init__()
        self.set_bigend = set_bigend

    def execute(self, processor):
        processor.registers.cpsr.set_e(self.set_bigend)
