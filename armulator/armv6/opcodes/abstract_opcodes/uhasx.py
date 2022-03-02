from armulator.armv6.bits_ops import substring, set_substring
from armulator.armv6.opcodes.opcode import Opcode


class Uhasx(Opcode):
    def __init__(self, instruction, m, d, n):
        super().__init__(instruction)
        self.m = m
        self.d = d
        self.n = n

    def execute(self, processor):
        if processor.condition_passed():
            n = processor.registers.get(self.n)
            m = processor.registers.get(self.m)
            diff = substring(n, 15, 0) - substring(m, 31, 16)
            sum_ = substring(n, 31, 16) + substring(m, 15, 0)
            d = set_substring(0, 15, 0, substring(diff, 16, 1))
            d = set_substring(d, 31, 16, substring(sum_, 16, 1))
            processor.registers.set(self.d, d)
