from armulator.armv6.bits_ops import substring, set_substring, lower_chunk
from armulator.armv6.opcodes.opcode import Opcode


class Uadd16(Opcode):
    def __init__(self, instruction, m, d, n):
        super().__init__(instruction)
        self.m = m
        self.d = d
        self.n = n

    def execute(self, processor):
        if processor.condition_passed():
            n = processor.registers.get(self.n)
            m = processor.registers.get(self.m)
            sum1 = substring(n, 15, 0) + substring(m, 15, 0)
            sum2 = substring(n, 31, 16) + substring(m, 31, 16)
            d = set_substring(0, 15, 0, lower_chunk(sum1, 16))
            d = set_substring(d, 31, 16, lower_chunk(sum2, 16))
            processor.registers.set(self.d, d)
            ge = 0b11 if sum1 >= 0x10000 else 00
            ge = set_substring(ge, 3, 2, 0b11 if sum2 >= 0x10000 else 00)
            processor.registers.cpsr.ge = ge
