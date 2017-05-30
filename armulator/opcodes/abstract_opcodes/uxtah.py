from armulator.opcodes.abstract_opcode import AbstractOpcode
from armulator.shift import ror
from armulator.bits_ops import add, zero_extend


class Uxtah(AbstractOpcode):
    def __init__(self, m, d, n, rotation):
        super(Uxtah, self).__init__()
        self.m = m
        self.d = d
        self.n = n
        self.rotation = rotation

    def execute(self, processor):
        if processor.condition_passed():
            rotated = ror(processor.registers.get(self.m), self.rotation)
            processor.registers.set(self.d,
                                         add(processor.registers.get(self.n), zero_extend(rotated[16:32], 32), 32))
