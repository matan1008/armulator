from armulator.opcodes.abstract_opcode import AbstractOpcode
from armulator.shift import ror
from armulator.bits_ops import zero_extend


class Uxth(AbstractOpcode):
    def __init__(self, m, d, rotation):
        super(Uxth, self).__init__()
        self.m = m
        self.d = d
        self.rotation = rotation

    def execute(self, processor):
        if processor.condition_passed():
            rotated = ror(processor.core_registers.get(self.m), self.rotation)
            processor.core_registers.set(self.d, zero_extend(rotated[16:32], 32))
