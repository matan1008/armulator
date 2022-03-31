from armulator.armv6.bits_ops import sign_extend, substring, set_substring
from armulator.armv6.opcodes.opcode import Opcode
from armulator.armv6.shift import ror


class Sxtb16(Opcode):
    def __init__(self, instruction, m, d, rotation):
        super().__init__(instruction)
        self.m = m
        self.d = d
        self.rotation = rotation

    def execute(self, processor):
        if processor.condition_passed():
            rotated = ror(processor.registers.get(self.m), 32, self.rotation)
            temp_rd = set_substring(0, 15, 0, sign_extend(substring(rotated, 7, 0), 8, 16))
            temp_rd = set_substring(temp_rd, 31, 16, sign_extend(substring(rotated, 23, 16), 8, 16))
            processor.registers.set(self.d, temp_rd)
