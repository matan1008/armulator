from armulator.armv6.bits_ops import set_substring, to_signed, substring, to_unsigned
from armulator.armv6.opcodes.opcode import Opcode


class Shadd8(Opcode):
    def __init__(self, instruction, m, d, n):
        super().__init__(instruction)
        self.m = m
        self.d = d
        self.n = n

    def execute(self, processor):
        if processor.condition_passed():
            n = processor.registers.get(self.n)
            m = processor.registers.get(self.m)
            sum1 = to_signed(substring(n, 7, 0), 8) + to_signed(substring(m, 7, 0), 8)
            sum2 = to_signed(substring(n, 15, 8), 8) + to_signed(substring(m, 15, 8), 8)
            sum3 = to_signed(substring(n, 23, 16), 8) + to_signed(substring(m, 23, 16), 8)
            sum4 = to_signed(substring(n, 31, 24), 8) + to_signed(substring(m, 31, 24), 8)
            d = set_substring(0, 7, 0, to_unsigned(sum1, 9) >> 1)
            d = set_substring(d, 15, 8, to_unsigned(sum2, 9) >> 1)
            d = set_substring(d, 23, 16, to_unsigned(sum3, 9) >> 1)
            d = set_substring(d, 31, 24, to_unsigned(sum4, 9) >> 1)
            processor.registers.set(self.d, d)
