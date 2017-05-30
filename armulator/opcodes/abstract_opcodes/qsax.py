from armulator.opcodes.abstract_opcode import AbstractOpcode
from armulator.bits_ops import signed_sat


class Qsax(AbstractOpcode):
    def __init__(self, m, d, n):
        super(Qsax, self).__init__()
        self.m = m
        self.d = d
        self.n = n

    def execute(self, processor):
        if processor.condition_passed():
            sum_ = processor.registers.get(self.n)[16:32].int + processor.registers.get(self.m)[0:16].int
            diff = processor.registers.get(self.n)[0:16].int - processor.registers.get(self.m)[16:32].int
            processor.registers.set(self.d, signed_sat(diff, 16) + signed_sat(sum_, 16))
