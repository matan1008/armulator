from armulator.opcodes.abstract_opcode import AbstractOpcode
from armulator.shift import ror
from armulator.bits_ops import add, sign_extend


class Sxtab16(AbstractOpcode):
    def __init__(self, m, d, n, rotation):
        super(Sxtab16, self).__init__()
        self.m = m
        self.d = d
        self.n = n
        self.rotation = rotation

    def execute(self, processor):
        if processor.condition_passed():
            rotated = ror(processor.registers.get(self.m), self.rotation)
            temp_rd = add(processor.registers.get(self.n)[0:16], sign_extend(rotated[8:16], 16), 16)
            temp_rd += add(processor.registers.get(self.n)[16:32], sign_extend(rotated[24:32], 16), 16)
            processor.registers.set(self.d, temp_rd)
