from armulator.armv6.opcodes.abstract_opcode import AbstractOpcode
from armulator.armv6.shift import shift_c


class TstRegisterShiftedRegister(AbstractOpcode):
    def __init__(self, m, s, n, shift_t):
        super(TstRegisterShiftedRegister, self).__init__()
        self.m = m
        self.s = s
        self.n = n
        self.shift_t = shift_t

    def execute(self, processor):
        shift_n = processor.registers.get(self.s)[24:32].uint
        shifted, carry = shift_c(processor.registers.get(self.m), self.shift_t, shift_n,
                                 processor.registers.cpsr.get_c())
        result = processor.registers.get(self.n) & shifted
        processor.registers.cpsr.set_n(result[0])
        processor.registers.cpsr.set_z(not result.any(True))
        processor.registers.cpsr.set_c(carry)
