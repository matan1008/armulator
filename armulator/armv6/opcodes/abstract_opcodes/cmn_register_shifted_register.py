from armulator.armv6.bits_ops import add_with_carry, lower_chunk, bit_at
from armulator.armv6.opcodes.opcode import Opcode
from armulator.armv6.shift import shift


class CmnRegisterShiftedRegister(Opcode):
    def __init__(self, instruction, m, s, n, shift_t):
        super().__init__(instruction)
        self.m = m
        self.s = s
        self.n = n
        self.shift_t = shift_t

    def execute(self, processor):
        shift_n = lower_chunk(processor.registers.get(self.s), 8)
        shifted = shift(processor.registers.get(self.m), 32, self.shift_t, shift_n, processor.registers.cpsr.c)
        result, carry, overflow = add_with_carry(processor.registers.get(self.n), shifted, 0)
        processor.registers.cpsr.n = bit_at(result, 31)
        processor.registers.cpsr.z = 0 if result else 1
        processor.registers.cpsr.c = carry
        processor.registers.cpsr.v = overflow
