from armulator.armv6.bits_ops import add_with_carry, bit_at
from armulator.armv6.opcodes.opcode import Opcode


class CmnImmediate(Opcode):
    def __init__(self, instruction, n, imm32):
        super().__init__(instruction)
        self.n = n
        self.imm32 = imm32

    def execute(self, processor):
        if processor.condition_passed():
            result, carry, overflow = add_with_carry(processor.registers.get(self.n), self.imm32, 0)
            processor.registers.cpsr.n = bit_at(result, 31)
            processor.registers.cpsr.z = 0 if result else 1
            processor.registers.cpsr.c = carry
            processor.registers.cpsr.v = overflow
