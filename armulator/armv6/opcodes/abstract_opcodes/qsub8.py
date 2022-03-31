from armulator.armv6.bits_ops import signed_sat, set_substring, to_signed, substring
from armulator.armv6.opcodes.opcode import Opcode


class Qsub8(Opcode):
    def __init__(self, instruction, m, d, n):
        super().__init__(instruction)
        self.m = m
        self.d = d
        self.n = n

    def execute(self, processor):
        if processor.condition_passed():
            n = processor.registers.get(self.n)
            m = processor.registers.get(self.m)
            diff1 = to_signed(substring(n, 7, 0), 8) - to_signed(substring(m, 7, 0), 8)
            diff2 = to_signed(substring(n, 15, 8), 8) - to_signed(substring(m, 15, 8), 8)
            diff3 = to_signed(substring(n, 23, 16), 8) - to_signed(substring(m, 23, 16), 8)
            diff4 = to_signed(substring(n, 31, 24), 8) - to_signed(substring(m, 31, 24), 8)
            d = set_substring(0, 7, 0, signed_sat(diff1, 8))
            d = set_substring(d, 15, 8, signed_sat(diff2, 8))
            d = set_substring(d, 23, 16, signed_sat(diff3, 8))
            d = set_substring(d, 31, 24, signed_sat(diff4, 8))
            processor.registers.set(self.d, d)
