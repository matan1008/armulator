from armulator.armv6.bits_ops import bit_at
from armulator.armv6.opcodes.opcode import Opcode


class TeqImmediate(Opcode):
    def __init__(self, instruction, n, imm32, carry):
        super().__init__(instruction)
        self.n = n
        self.imm32 = imm32
        self.carry = carry

    def execute(self, processor):
        if processor.condition_passed():
            result = processor.registers.get(self.n) ^ self.imm32
            processor.registers.cpsr.n = bit_at(result, 31)
            processor.registers.cpsr.z = 0 if result else 1
            processor.registers.cpsr.c = self.carry
