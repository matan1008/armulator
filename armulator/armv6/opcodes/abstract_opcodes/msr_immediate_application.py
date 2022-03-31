from armulator.armv6.bits_ops import bit_at, substring
from armulator.armv6.opcodes.opcode import Opcode


class MsrImmediateApplication(Opcode):
    def __init__(self, instruction, write_nzcvq, write_g, imm32):
        super().__init__(instruction)
        self.write_nzcvq = write_nzcvq
        self.write_g = write_g
        self.imm32 = imm32

    def execute(self, processor):
        if processor.condition_passed():
            if self.write_nzcvq:
                processor.registers.cpsr.n = bit_at(self.imm32, 31)
                processor.registers.cpsr.z = bit_at(self.imm32, 30)
                processor.registers.cpsr.c = bit_at(self.imm32, 29)
                processor.registers.cpsr.v = bit_at(self.imm32, 28)
                processor.registers.cpsr.q = bit_at(self.imm32, 27)
            if self.write_g:
                processor.registers.cpsr.ge = substring(self.imm32, 19, 16)
