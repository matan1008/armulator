from armulator.armv6.bits_ops import bit_at, bit_not
from armulator.armv6.opcodes.opcode import Opcode


class OrnImmediate(Opcode):
    def __init__(self, instruction, setflags, d, n, imm32, carry):
        super().__init__(instruction)
        self.setflags = setflags
        self.d = d
        self.n = n
        self.imm32 = imm32
        self.carry = carry

    def execute(self, processor):
        if processor.condition_passed():
            result = processor.registers.get(self.n) | bit_not(self.imm32, 32)
            processor.registers.set(self.d, result)
            if self.setflags:
                processor.registers.cpsr.n = bit_at(result, 31)
                processor.registers.cpsr.z = 0 if result else 1
                processor.registers.cpsr.c = self.carry
