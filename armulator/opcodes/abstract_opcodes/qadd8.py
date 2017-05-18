from armulator.opcodes.abstract_opcode import AbstractOpcode
from armulator.bits_ops import signed_sat


class Qadd8(AbstractOpcode):
    def __init__(self, m, d, n):
        super(Qadd8, self).__init__()
        self.m = m
        self.d = d
        self.n = n

    def execute(self, processor):
        if processor.condition_passed():
            sum1 = processor.core_registers.get(self.n)[24:32].int + processor.core_registers.get(self.m)[24:32].int
            sum2 = processor.core_registers.get(self.n)[16:24].int + processor.core_registers.get(self.m)[16:24].int
            sum3 = processor.core_registers.get(self.n)[8:16].int + processor.core_registers.get(self.m)[8:16].int
            sum4 = processor.core_registers.get(self.n)[0:8].int + processor.core_registers.get(self.m)[0:8].int
            signed_sum = signed_sat(sum4, 8) + signed_sat(sum3, 8) + signed_sat(sum2, 8) + signed_sat(sum1, 8)
            processor.core_registers.set(self.d, signed_sum)
