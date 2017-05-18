from armulator.opcodes.abstract_opcode import AbstractOpcode
from armulator.shift import shift_c


class TstRegisterShiftedRegister(AbstractOpcode):
    def __init__(self, m, s, n, shift_t):
        super(TstRegisterShiftedRegister, self).__init__()
        self.m = m
        self.s = s
        self.n = n
        self.shift_t = shift_t

    def execute(self, processor):
        shift_n = processor.core_registers.get(self.s)[24:32].uint
        shifted, carry = shift_c(processor.core_registers.get(self.m), self.shift_t, shift_n,
                                 processor.core_registers.get_cpsr_c())
        result = processor.core_registers.get(self.n) & shifted
        processor.core_registers.set_cpsr_n(result[0])
        processor.core_registers.set_cpsr_z(not result.any(True))
        processor.core_registers.set_cpsr_c(carry)
