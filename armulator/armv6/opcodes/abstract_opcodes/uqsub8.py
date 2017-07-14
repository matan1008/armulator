from armulator.armv6.opcodes.abstract_opcode import AbstractOpcode
from armulator.armv6.bits_ops import unsigned_sat


class Uqsub8(AbstractOpcode):
    def __init__(self, m, d, n):
        super(Uqsub8, self).__init__()
        self.m = m
        self.d = d
        self.n = n

    def execute(self, processor):
        if processor.condition_passed():
            diff1 = processor.registers.get(self.n)[24:32].uint - processor.registers.get(self.m)[24:32].uint
            diff2 = processor.registers.get(self.n)[16:24].uint - processor.registers.get(self.m)[16:24].uint
            diff3 = processor.registers.get(self.n)[8:16].uint - processor.registers.get(self.m)[8:16].uint
            diff4 = processor.registers.get(self.n)[0:8].uint - processor.registers.get(self.m)[0:8].uint
            processor.registers.set(
                    self.d,
                    unsigned_sat(diff4, 8) + unsigned_sat(diff3, 8) + unsigned_sat(diff2, 8) + unsigned_sat(diff1, 8)
            )
