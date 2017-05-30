from armulator.opcodes.abstract_opcode import AbstractOpcode
from bitstring import BitArray


class Shadd16(AbstractOpcode):
    def __init__(self, m, d, n):
        super(Shadd16, self).__init__()
        self.m = m
        self.d = d
        self.n = n

    def execute(self, processor):
        if processor.condition_passed():
            sum1 = processor.registers.get(self.n)[16:32].int + processor.registers.get(self.m)[16:32].int
            sum2 = processor.registers.get(self.n)[0:16].int + processor.registers.get(self.m)[0:16].int
            processor.registers.set(self.d,
                                         BitArray(int=sum2, length=17)[0:16] + BitArray(int=sum1, length=17)[0:16])
