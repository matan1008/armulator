from armulator.armv6.opcodes.abstract_opcode import AbstractOpcode
from armulator.armv6.shift import shift_c, SRType


class LslRegister(AbstractOpcode):
    def __init__(self, setflags, m, d, n):
        super(LslRegister, self).__init__()
        self.setflags = setflags
        self.m = m
        self.d = d
        self.n = n

    def execute(self, processor):
        shift_n = processor.registers.get(self.m)[24:32].uint
        result, carry = shift_c(processor.registers.get(self.n), SRType.SRType_LSL, shift_n,
                                processor.registers.cpsr.get_c())
        processor.registers.set(self.d, result)
        if self.setflags:
            processor.registers.cpsr.set_n(result[0])
            processor.registers.cpsr.set_z(not result.any(True))
            processor.registers.cpsr.set_c(carry)
