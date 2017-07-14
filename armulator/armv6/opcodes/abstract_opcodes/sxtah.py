from armulator.armv6.opcodes.abstract_opcode import AbstractOpcode
from armulator.armv6.shift import ror
from armulator.armv6.bits_ops import add, sign_extend


class Sxtah(AbstractOpcode):
    def __init__(self, m, d, n, rotation):
        super(Sxtah, self).__init__()
        self.m = m
        self.d = d
        self.n = n
        self.rotation = rotation

    def execute(self, processor):
        if processor.condition_passed():
            rotated = ror(processor.registers.get(self.m), self.rotation)
            processor.registers.set(self.d, add(processor.registers.get(self.n), sign_extend(rotated[16:32], 32), 32))
