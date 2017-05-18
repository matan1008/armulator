from armulator.opcodes.abstract_opcode import AbstractOpcode
from armulator.shift import shift_c


class BicRegisterShiftedRegister(AbstractOpcode):
    def __init__(self, setflags, m, s, d, n, shift_t):
        super(BicRegisterShiftedRegister, self).__init__()
        self.setflags = setflags
        self.m = m
        self.s = s
        self.d = d
        self.n = n
        self.shift_t = shift_t

    def execute(self, processor):
        shift_n = processor.core_registers.get(self.s)[24:32].uint
        shifted, carry = shift_c(processor.core_registers.get(self.m), self.shift_t, shift_n,
                                 processor.core_registers.get_cpsr_c())
        result = processor.core_registers.get(self.n) & ~shifted
        processor.core_registers.set(self.d, result)
        if self.setflags:
            processor.core_registers.set_cpsr_n(result[0])
            processor.core_registers.set_cpsr_z(not result.any(True))
            processor.core_registers.set_cpsr_c(carry)
