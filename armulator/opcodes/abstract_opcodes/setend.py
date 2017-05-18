from armulator.opcodes.abstract_opcode import AbstractOpcode


class Setend(AbstractOpcode):
    def __init__(self, set_bigend):
        super(Setend, self).__init__()
        self.set_bigend = set_bigend

    def execute(self, processor):
        processor.core_registers.set_cpsr_e(self.set_bigend)
