from armulator.armv6.bits_ops import set_bit_at, set_substring, substring, lower_chunk
from armulator.armv6.opcodes.opcode import Opcode


class Uadd8(Opcode):
    def __init__(self, instruction, m, d, n):
        super().__init__(instruction)
        self.m = m
        self.d = d
        self.n = n

    def execute(self, processor):
        if processor.condition_passed():
            n = processor.registers.get(self.n)
            m = processor.registers.get(self.m)
            sum1 = substring(n, 7, 0) + substring(m, 7, 0)
            sum2 = substring(n, 15, 8) + substring(m, 15, 8)
            sum3 = substring(n, 23, 16) + substring(m, 23, 16)
            sum4 = substring(n, 31, 24) + substring(m, 31, 24)
            d = set_substring(0, 7, 0, lower_chunk(sum1, 8))
            d = set_substring(d, 15, 8, lower_chunk(sum2, 8))
            d = set_substring(d, 23, 16, lower_chunk(sum3, 8))
            d = set_substring(d, 31, 24, lower_chunk(sum4, 8))
            processor.registers.set(self.d, d)
            ge = set_bit_at(0, 0, 0b1 if sum1 >= 0x100 else 0b0)
            ge = set_bit_at(ge, 1, 0b1 if sum2 >= 0x100 else 0b0)
            ge = set_bit_at(ge, 2, 0b1 if sum3 >= 0x100 else 0b0)
            ge = set_bit_at(ge, 3, 0b1 if sum4 >= 0x100 else 0b0)
            processor.registers.cpsr.ge = ge
