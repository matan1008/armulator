from armulator.armv6.opcodes.abstract_opcode import AbstractOpcode
from armulator.armv6.shift import shift
from armulator.armv6.bits_ops import add_with_carry


class RscRegisterShiftedRegister(AbstractOpcode):
    def __init__(self, setflags, m, s, d, n, shift_t):
        super(RscRegisterShiftedRegister, self).__init__()
        self.setflags = setflags
        self.m = m
        self.s = s
        self.d = d
        self.n = n
        self.shift_t = shift_t

    def execute(self, processor):
        shift_n = processor.registers.get(self.s)[24:32].uint
        shifted = shift(processor.registers.get(self.m), self.shift_t, shift_n,
                        processor.registers.cpsr.get_c())
        result, carry, overflow = add_with_carry(~processor.registers.get(self.n), shifted,
                                                 processor.registers.cpsr.get_c())
        processor.registers.set(self.d, result)
        if self.setflags:
            processor.registers.cpsr.set_n(result[0])
            processor.registers.cpsr.set_z(not result.any(True))
            processor.registers.cpsr.set_c(carry)
            processor.registers.cpsr.set_v(overflow)
