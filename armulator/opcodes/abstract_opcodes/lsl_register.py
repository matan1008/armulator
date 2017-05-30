from armulator.opcodes.abstract_opcode import AbstractOpcode
from armulator.shift import shift_c, SRType


class LslRegister(AbstractOpcode):
    def __init__(self, setflags, m, d, n):
        super(LslRegister, self).__init__()
        self.setflags = setflags
        self.m = m
        self.d = d
        self.n = n

    def execute(self, processor):
        shift_n = processor.core_registers.get(self.m)[24:32].uint
        result, carry = shift_c(processor.core_registers.get(self.n), SRType.SRType_LSL, shift_n,
                                processor.core_registers.cpsr.get_c())
        processor.core_registers.set(self.d, result)
        if self.setflags:
            processor.core_registers.cpsr.set_n(result[0])
            processor.core_registers.cpsr.set_z(not result.any(True))
            processor.core_registers.cpsr.set_c(carry)
