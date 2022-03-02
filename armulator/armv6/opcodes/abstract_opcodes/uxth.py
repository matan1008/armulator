from armulator.armv6.bits_ops import lower_chunk
from armulator.armv6.opcodes.opcode import Opcode
from armulator.armv6.shift import ror


class Uxth(Opcode):
    def __init__(self, instruction, m, d, rotation):
        super().__init__(instruction)
        self.m = m
        self.d = d
        self.rotation = rotation

    def execute(self, processor):
        if processor.condition_passed():
            rotated = ror(processor.registers.get(self.m), 32, self.rotation)
            processor.registers.set(self.d, lower_chunk(rotated, 16))
