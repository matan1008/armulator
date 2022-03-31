from armulator.armv6.bits_ops import substring, set_substring, bit_at
from armulator.armv6.opcodes.opcode import Opcode


class Sel(Opcode):
    def __init__(self, instruction, m, d, n):
        super().__init__(instruction)
        self.m = m
        self.d = d
        self.n = n

    def execute(self, processor):
        if processor.condition_passed():
            ge = processor.registers.cpsr.ge
            n = processor.registers.get(self.n)
            m = processor.registers.get(self.m)
            temp_rd = set_substring(0, 7, 0, substring(n if bit_at(ge, 0) else m, 7, 0))
            temp_rd = set_substring(temp_rd, 15, 8, substring(n if bit_at(ge, 1) else m, 15, 8))
            temp_rd = set_substring(temp_rd, 23, 16, substring(n if bit_at(ge, 2) else m, 23, 16))
            temp_rd = set_substring(temp_rd, 31, 24, substring(n if bit_at(ge, 3) else m, 31, 24))
            processor.registers.set(self.d, temp_rd)
