from armulator.armv6.opcodes.abstract_opcode import AbstractOpcode
from armulator.armv6.shift import shift_c


class TeqRegister(AbstractOpcode):
    def __init__(self, m, n, shift_t, shift_n):
        super(TeqRegister, self).__init__()
        self.m = m
        self.n = n
        self.shift_t = shift_t
        self.shift_n = shift_n

    def execute(self, processor):
        if processor.condition_passed():
            shifted, carry = shift_c(processor.registers.get(self.m), self.shift_t, self.shift_n,
                                     processor.registers.cpsr.get_c())
            result = processor.registers.get(self.n) ^ shifted
            processor.registers.cpsr.set_n(result[0])
            processor.registers.cpsr.set_z(not result.any(True))
            processor.registers.cpsr.set_c(carry)
