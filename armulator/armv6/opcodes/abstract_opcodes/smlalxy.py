from armulator.armv6.bits_ops import substring, set_substring, to_signed, to_unsigned
from armulator.armv6.opcodes.opcode import Opcode


class Smlalxy(Opcode):
    def __init__(self, instruction, m_high, n_high, m, d_hi, d_lo, n):
        super().__init__(instruction)
        self.m_high = m_high
        self.n_high = n_high
        self.m = m
        self.d_hi = d_hi
        self.d_lo = d_lo
        self.n = n

    def execute(self, processor):
        if processor.condition_passed():
            n = processor.registers.get(self.n)
            operand1 = substring(n, 31, 16) if self.n_high else substring(n, 15, 0)
            m = processor.registers.get(self.m)
            operand2 = substring(m, 31, 16) if self.m_high else substring(m, 15, 0)
            d_total = to_signed(
                set_substring(processor.registers.get(self.d_lo), 63, 32, processor.registers.get(self.d_hi)), 64
            )
            result = to_unsigned(to_signed(operand1, 16) * to_signed(operand2, 16) + d_total, 64)
            processor.registers.set(self.d_hi, substring(result, 63, 32))
            processor.registers.set(self.d_lo, substring(result, 31, 0))
