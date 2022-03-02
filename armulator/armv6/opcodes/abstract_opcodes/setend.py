from armulator.armv6.opcodes.opcode import Opcode


class Setend(Opcode):
    def __init__(self, instruction, set_bigend):
        super().__init__(instruction)
        self.set_bigend = set_bigend

    def execute(self, processor):
        processor.registers.cpsr.e = self.set_bigend
