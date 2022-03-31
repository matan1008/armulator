from armulator.armv6.bits_ops import substring, set_substring
from armulator.armv6.opcodes.opcode import Opcode


class Uhsub8(Opcode):
    def __init__(self, instruction, m, d, n):
        super().__init__(instruction)
        self.m = m
        self.d = d
        self.n = n

    def execute(self, processor):
        if processor.condition_passed():
            n = processor.registers.get(self.n)
            m = processor.registers.get(self.m)
            diff1 = substring(n, 7, 0) - substring(m, 7, 0)
            diff2 = substring(n, 15, 8) - substring(m, 15, 8)
            diff3 = substring(n, 23, 16) - substring(m, 23, 16)
            diff4 = substring(n, 31, 24) - substring(m, 31, 24)
            d = set_substring(0, 7, 0, substring(diff1, 8, 1))
            d = set_substring(d, 15, 8, substring(diff2, 8, 1))
            d = set_substring(d, 23, 16, substring(diff3, 8, 1))
            d = set_substring(d, 31, 24, substring(diff4, 8, 1))
            processor.registers.set(self.d, d)
