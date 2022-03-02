from armulator.armv6.bits_ops import add, lower_chunk
from armulator.armv6.opcodes.opcode import Opcode
from armulator.armv6.shift import ror


class Uxtab(Opcode):
    def __init__(self, instruction, m, d, n, rotation):
        super().__init__(instruction)
        self.m = m
        self.d = d
        self.n = n
        self.rotation = rotation

    def execute(self, processor):
        if processor.condition_passed():
            rotated = ror(processor.registers.get(self.m), 32, self.rotation)
            processor.registers.set(self.d, add(processor.registers.get(self.n), lower_chunk(rotated, 8), 32))
