from armulator.opcodes.abstract_opcode import AbstractOpcode
from armulator.shift import shift_c


class TstRegister(AbstractOpcode):
    def __init__(self, m, n, shift_t, shift_n):
        super(TstRegister, self).__init__()
        self.m = m
        self.n = n
        self.shift_t = shift_t
        self.shift_n = shift_n

    def execute(self, processor):
        if processor.condition_passed():
            shifted, carry = shift_c(processor.core_registers.get(self.m), self.shift_t, self.shift_n,
                                     processor.core_registers.cpsr.get_c())
            result = processor.core_registers.get(self.n) & shifted
            processor.core_registers.cpsr.set_n(result[0])
            processor.core_registers.cpsr.set_z(not result.any(True))
            processor.core_registers.cpsr.set_c(carry)
