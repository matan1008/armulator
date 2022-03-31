from armulator.armv6.bits_ops import set_substring
from armulator.armv6.opcodes.opcode import Opcode


class Movt(Opcode):
    def __init__(self, instruction, d, imm16):
        super().__init__(instruction)
        self.d = d
        self.imm16 = imm16

    def execute(self, processor):
        if processor.condition_passed():
            processor.registers.set(self.d, set_substring(processor.registers.get(self.d), 31, 16, self.imm16))
