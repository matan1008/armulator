from armulator.armv6.bits_ops import add, sign_extend, substring, set_substring
from armulator.armv6.opcodes.opcode import Opcode
from armulator.armv6.shift import ror


class Sxtab16(Opcode):
    def __init__(self, instruction, m, d, n, rotation):
        super().__init__(instruction)
        self.m = m
        self.d = d
        self.n = n
        self.rotation = rotation

    def execute(self, processor):
        if processor.condition_passed():
            rotated = ror(processor.registers.get(self.m), 32, self.rotation)
            n = processor.registers.get(self.n)
            lower_half = add(substring(n, 15, 0), sign_extend(substring(rotated, 7, 0), 8, 16), 16)
            temp_rd = set_substring(0, 15, 0, lower_half)
            upper_half = add(substring(n, 31, 16), sign_extend(substring(rotated, 23, 16), 8, 16), 16)
            temp_rd = set_substring(temp_rd, 31, 16, upper_half)
            processor.registers.set(self.d, temp_rd)
