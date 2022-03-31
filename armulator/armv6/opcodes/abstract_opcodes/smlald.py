from armulator.armv6.bits_ops import to_signed, substring, set_substring, to_unsigned
from armulator.armv6.opcodes.opcode import Opcode
from armulator.armv6.shift import ror


class Smlald(Opcode):
    def __init__(self, instruction, m_swap, m, d_hi, d_lo, n):
        super().__init__(instruction)
        self.m_swap = m_swap
        self.m = m
        self.d_hi = d_hi
        self.d_lo = d_lo
        self.n = n

    def execute(self, processor):
        if processor.condition_passed():
            operand2 = ror(processor.registers.get(self.m), 32, 16) if self.m_swap else processor.registers.get(self.m)
            n = processor.registers.get(self.n)
            product1 = to_signed(substring(n, 15, 0), 16) * to_signed(substring(operand2, 15, 0), 16)
            product2 = to_signed(substring(n, 31, 16), 16) * to_signed(substring(operand2, 31, 16), 16)
            d_total = to_signed(
                set_substring(processor.registers.get(self.d_lo), 63, 32, processor.registers.get(self.d_hi)), 64
            )
            result = to_unsigned(product1 + product2 + d_total, 64)
            processor.registers.set(self.d_hi, substring(result, 63, 32))
            processor.registers.set(self.d_lo, substring(result, 31, 0))
