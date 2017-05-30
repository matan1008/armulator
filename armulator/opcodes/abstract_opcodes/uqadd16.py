from armulator.opcodes.abstract_opcode import AbstractOpcode
from armulator.bits_ops import unsigned_sat


class Uqadd16(AbstractOpcode):
    def __init__(self, m, d, n):
        super(Uqadd16, self).__init__()
        self.m = m
        self.d = d
        self.n = n

    def execute(self, processor):
        if processor.condition_passed():
            sum1 = processor.registers.get(self.n)[16:32].uint + processor.registers.get(self.m)[16:32].uint
            sum2 = processor.registers.get(self.n)[0:16].uint + processor.registers.get(self.m)[0:16].uint
            processor.registers.set(self.d, unsigned_sat(sum2, 16) + unsigned_sat(sum1, 16))
