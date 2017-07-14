from armulator.armv6.opcodes.abstract_opcode import AbstractOpcode
from armulator.armv6.bits_ops import signed_sat


class Qsub16(AbstractOpcode):
    def __init__(self, m, d, n):
        super(Qsub16, self).__init__()
        self.m = m
        self.d = d
        self.n = n

    def execute(self, processor):
        if processor.condition_passed():
            diff1 = processor.registers.get(self.n)[16:32].int - processor.registers.get(self.m)[16:32].int
            diff2 = processor.registers.get(self.n)[0:16].int - processor.registers.get(self.m)[0:16].int
            processor.registers.set(self.d, signed_sat(diff2, 16) + signed_sat(diff1, 16))
