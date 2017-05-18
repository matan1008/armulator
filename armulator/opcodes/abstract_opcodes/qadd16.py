from armulator.opcodes.abstract_opcode import AbstractOpcode
from armulator.bits_ops import signed_sat


class Qadd16(AbstractOpcode):
    def __init__(self, m, d, n):
        super(Qadd16, self).__init__()
        self.m = m
        self.d = d
        self.n = n

    def execute(self, processor):
        if processor.condition_passed():
            sum1 = processor.core_registers.get(self.n)[16:32].int + processor.core_registers.get(self.m)[16:32].int
            sum2 = processor.core_registers.get(self.n)[0:16].int + processor.core_registers.get(self.m)[0:16].int
            processor.core_registers.set(self.d, signed_sat(sum2, 16) + signed_sat(sum1, 16))
