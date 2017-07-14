from armulator.armv6.opcodes.abstract_opcode import AbstractOpcode
from bitstring import BitArray


class Usad8(AbstractOpcode):
    def __init__(self, m, d, n):
        super(Usad8, self).__init__()
        self.m = m
        self.d = d
        self.n = n

    def execute(self, processor):
        if processor.condition_passed():
            absdiff1 = abs(
                processor.registers.get(self.n)[24:32].uint - processor.registers.get(self.m)[24:32].uint)
            absdiff2 = abs(
                processor.registers.get(self.n)[16:24].uint - processor.registers.get(self.m)[16:24].uint)
            absdiff3 = abs(
                processor.registers.get(self.n)[8:16].uint - processor.registers.get(self.m)[8:16].uint)
            absdiff4 = abs(
                processor.registers.get(self.n)[0:8].uint - processor.registers.get(self.m)[0:8].uint)
            result = absdiff1 + absdiff2 + absdiff3 + absdiff4
            processor.registers.set(self.d, BitArray(uint=result, length=32))
