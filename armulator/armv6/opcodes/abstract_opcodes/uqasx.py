from armulator.armv6.opcodes.abstract_opcode import AbstractOpcode
from armulator.armv6.bits_ops import unsigned_sat


class Uqasx(AbstractOpcode):
    def __init__(self, m, d, n):
        super(Uqasx, self).__init__()
        self.m = m
        self.d = d
        self.n = n

    def execute(self, processor):
        if processor.condition_passed():
            diff = processor.registers.get(self.n)[16:32].uint - processor.registers.get(self.m)[0:16].uint
            sum_ = processor.registers.get(self.n)[0:16].uint + processor.registers.get(self.m)[16:32].uint
            processor.registers.set(self.d, unsigned_sat(sum_, 16) + unsigned_sat(diff, 16))
