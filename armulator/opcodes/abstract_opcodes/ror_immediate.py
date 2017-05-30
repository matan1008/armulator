from armulator.opcodes.abstract_opcode import AbstractOpcode
from armulator.shift import shift_c, SRType


class RorImmediate(AbstractOpcode):
    def __init__(self, setflags, m, d, shift_n):
        super(RorImmediate, self).__init__()
        self.setflags = setflags
        self.m = m
        self.d = d
        self.shift_n = shift_n

    def execute(self, processor):
        if processor.condition_passed():
            result, carry = shift_c(processor.core_registers.get(self.m), SRType.SRType_ROR, self.shift_n,
                                    processor.core_registers.cpsr.get_c())
            if self.d == 15:
                processor.alu_write_pc(result)
            else:
                processor.core_registers.set(self.d, result)
                if self.setflags:
                    processor.core_registers.cpsr.set_n(result[0])
                    processor.core_registers.cpsr.set_z(not result.any(True))
                    processor.core_registers.cpsr.set_c(carry)
