from armulator.opcodes.abstract_opcode import AbstractOpcode
from armulator.shift import shift_c, SRType


class LsrRegister(AbstractOpcode):
    def __init__(self, setflags, m, d, n):
        super(LsrRegister, self).__init__()
        self.setflags = setflags
        self.m = m
        self.d = d
        self.n = n

    def execute(self, processor):
        shift_n = processor.core_registers.get(self.m)[24:32].uint
        result, carry = shift_c(processor.core_registers.get(self.n), SRType.SRType_LSR, shift_n,
                                processor.core_registers.get_cpsr_c())
        processor.core_registers.set(self.d, result)
        if self.setflags:
            processor.core_registers.set_cpsr_n(result[0])
            processor.core_registers.set_cpsr_z(not result.any(True))
            processor.core_registers.set_cpsr_c(carry)
