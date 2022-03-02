from armulator.armv6.bits_ops import set_bit_at, set_substring, substring, lower_chunk
from armulator.armv6.opcodes.opcode import Opcode


class Usub8(Opcode):
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
            d = set_substring(0, 7, 0, lower_chunk(diff1, 8))
            d = set_substring(d, 15, 8, lower_chunk(diff2, 8))
            d = set_substring(d, 23, 16, lower_chunk(diff3, 8))
            d = set_substring(d, 31, 24, lower_chunk(diff4, 8))
            processor.registers.set(self.d, d)
            ge = set_bit_at(0, 0, 0b1 if diff1 >= 0 else 0b0)
            ge = set_bit_at(ge, 1, 0b1 if diff2 >= 0 else 0b0)
            ge = set_bit_at(ge, 2, 0b1 if diff3 >= 0 else 0b0)
            ge = set_bit_at(ge, 3, 0b1 if diff4 >= 0 else 0b0)
            processor.registers.cpsr.ge = ge
