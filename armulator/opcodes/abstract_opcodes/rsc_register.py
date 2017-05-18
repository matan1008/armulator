from armulator.opcodes.abstract_opcode import AbstractOpcode
from armulator.shift import shift
from armulator.bits_ops import add_with_carry


class RscRegister(AbstractOpcode):
    def __init__(self, setflags, m, d, n, shift_t, shift_n):
        super(RscRegister, self).__init__()
        self.setflags = setflags
        self.m = m
        self.d = d
        self.n = n
        self.shift_t = shift_t
        self.shift_n = shift_n

    def execute(self, processor):
        if processor.condition_passed():
            shifted = shift(processor.core_registers.get(self.m), self.shift_t, self.shift_n,
                            processor.core_registers.get_cpsr_c())
            result, carry, overflow = add_with_carry(~processor.core_registers.get(self.n), shifted,
                                                     processor.core_registers.get_cpsr_c())
            if self.d == 15:
                processor.alu_write_pc(result)
            else:
                processor.core_registers.set(self.d, result)
                if self.setflags:
                    processor.core_registers.set_cpsr_n(result[0])
                    processor.core_registers.set_cpsr_z(not result.any(True))
                    processor.core_registers.set_cpsr_c(carry)
                    processor.core_registers.set_cpsr_v(overflow)
