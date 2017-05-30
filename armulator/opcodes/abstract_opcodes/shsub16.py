from armulator.opcodes.abstract_opcode import AbstractOpcode
from bitstring import BitArray


class Shsub16(AbstractOpcode):
    def __init__(self, m, d, n):
        super(Shsub16, self).__init__()
        self.m = m
        self.d = d
        self.n = n

    def execute(self, processor):
        if processor.condition_passed():
            diff1 = processor.registers.get(self.n)[16:32].int - processor.registers.get(self.m)[16:32].int
            diff2 = processor.registers.get(self.n)[0:16].int - processor.registers.get(self.m)[0:16].int
            processor.registers.set(self.d, BitArray(int=diff2, length=17)[0:16] + BitArray(int=diff1, length=17)[0:16])
