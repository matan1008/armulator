from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.opcode import Opcode


class Usada8(Opcode):
    def __init__(self, instruction, m, a, d, n):
        super().__init__(instruction)
        self.m = m
        self.a = a
        self.d = d
        self.n = n

    def execute(self, processor):
        if processor.condition_passed():
            n = processor.registers.get(self.n)
            m = processor.registers.get(self.m)
            absdiff1 = abs(substring(n, 7, 0) - substring(m, 7, 0))
            absdiff2 = abs(substring(n, 15, 8) - substring(m, 15, 8))
            absdiff3 = abs(substring(n, 23, 16) - substring(m, 23, 16))
            absdiff4 = abs(substring(n, 31, 24) - substring(m, 31, 24))
            result = processor.registers.get(self.a) + absdiff1 + absdiff2 + absdiff3 + absdiff4
            processor.registers.set(self.d, substring(result, 31, 0))
