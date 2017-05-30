from armulator.opcodes.abstract_opcode import AbstractOpcode
from armulator.bits_ops import unsigned_sat


class Uqadd8(AbstractOpcode):
    def __init__(self, m, d, n):
        super(Uqadd8, self).__init__()
        self.m = m
        self.d = d
        self.n = n

    def execute(self, processor):
        if processor.condition_passed():
            sum1 = processor.registers.get(self.n)[24:32].uint + processor.registers.get(self.m)[24:32].uint
            sum2 = processor.registers.get(self.n)[16:24].uint + processor.registers.get(self.m)[16:24].uint
            sum3 = processor.registers.get(self.n)[8:16].uint + processor.registers.get(self.m)[8:16].uint
            sum4 = processor.registers.get(self.n)[0:8].uint + processor.registers.get(self.m)[0:8].uint
            processor.registers.set(
                    self.d,
                    unsigned_sat(sum4, 8) + unsigned_sat(sum3, 8) + unsigned_sat(sum2, 8) + unsigned_sat(sum1, 8)
            )
