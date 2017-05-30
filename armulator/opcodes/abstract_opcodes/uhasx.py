from armulator.opcodes.abstract_opcode import AbstractOpcode
from bitstring import BitArray


class Uhasx(AbstractOpcode):
    def __init__(self, m, d, n):
        super(Uhasx, self).__init__()
        self.m = m
        self.d = d
        self.n = n

    def execute(self, processor):
        if processor.condition_passed():
            diff = processor.registers.get(self.n)[16:32].uint - processor.registers.get(self.m)[0:16].uint
            sum_ = processor.registers.get(self.n)[0:16].uint + processor.registers.get(self.m)[16:32].uint
            processor.registers.set(self.d,
                                         BitArray(int=sum_, length=17)[0:16] + BitArray(int=diff, length=17)[0:16])
