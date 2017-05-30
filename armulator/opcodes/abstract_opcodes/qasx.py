from armulator.opcodes.abstract_opcode import AbstractOpcode
from armulator.bits_ops import signed_sat


class Qasx(AbstractOpcode):
    def __init__(self, m, d, n):
        super(Qasx, self).__init__()
        self.m = m
        self.d = d
        self.n = n

    def execute(self, processor):
        if processor.condition_passed():
            diff = processor.registers.get(self.n)[16:32].int - processor.registers.get(self.m)[0:16].int
            sum_ = processor.registers.get(self.n)[0:16].int + processor.registers.get(self.m)[16:32].int
            processor.registers.set(self.d, signed_sat(sum_, 16) + signed_sat(diff, 16))
