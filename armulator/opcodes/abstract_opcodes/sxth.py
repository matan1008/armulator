from armulator.opcodes.abstract_opcode import AbstractOpcode
from armulator.shift import ror
from armulator.bits_ops import sign_extend


class Sxth(AbstractOpcode):
    def __init__(self, m, d, rotation):
        super(Sxth, self).__init__()
        self.m = m
        self.d = d
        self.rotation = rotation

    def execute(self, processor):
        if processor.condition_passed():
            rotated = ror(processor.core_registers.get(self.m), self.rotation)
            processor.core_registers.set(self.d, sign_extend(rotated[16:32], 32))
