from armulator.armv6.bits_ops import set_substring, substring
from armulator.armv6.opcodes.opcode import Opcode
from armulator.armv6.shift import ror


class Uxtb16(Opcode):
    def __init__(self, instruction, m, d, rotation):
        super().__init__(instruction)
        self.m = m
        self.d = d
        self.rotation = rotation

    def execute(self, processor):
        if processor.condition_passed():
            rotated = ror(processor.registers.get(self.m), 32, self.rotation)
            temp_rd = set_substring(0, 15, 0, substring(rotated, 7, 0))
            temp_rd = set_substring(temp_rd, 31, 16, substring(rotated, 23, 16))
            processor.registers.set(self.d, temp_rd)
