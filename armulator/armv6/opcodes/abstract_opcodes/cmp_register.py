from armulator.armv6.opcodes.abstract_opcode import AbstractOpcode
from armulator.armv6.shift import shift
from armulator.armv6.bits_ops import add_with_carry


class CmpRegister(AbstractOpcode):
    def __init__(self, m, n, shift_t, shift_n):
        super(CmpRegister, self).__init__()
        self.m = m
        self.n = n
        self.shift_t = shift_t
        self.shift_n = shift_n

    def execute(self, processor):
        if processor.condition_passed():
            shifted = shift(processor.registers.get(self.m), self.shift_t, self.shift_n,
                            processor.registers.cpsr.get_c())
            result, carry, overflow = add_with_carry(processor.registers.get(self.n), ~shifted, "1")
            processor.registers.cpsr.set_n(result[0])
            processor.registers.cpsr.set_z(not result.any(True))
            processor.registers.cpsr.set_c(carry)
            processor.registers.cpsr.set_v(overflow)
