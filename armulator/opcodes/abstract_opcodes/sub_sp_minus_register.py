from armulator.opcodes.abstract_opcode import AbstractOpcode
from armulator.shift import shift
from armulator.bits_ops import add_with_carry


class SubSpMinusRegister(AbstractOpcode):
    def __init__(self, setflags, m, d, shift_t, shift_n):
        super(SubSpMinusRegister, self).__init__()
        self.setflags = setflags
        self.m = m
        self.d = d
        self.shift_t = shift_t
        self.shift_n = shift_n

    def execute(self, processor):
        if processor.condition_passed():
            shifted = shift(processor.registers.get(self.m), self.shift_t, self.shift_n,
                            processor.registers.cpsr.get_c())
            result, carry, overflow = add_with_carry(processor.registers.get_sp(), ~shifted, "1")
            if self.d == 15:
                processor.alu_write_pc(result)
            else:
                processor.registers.set(self.d, result)
                if self.setflags:
                    processor.registers.cpsr.set_n(result[0])
                    processor.registers.cpsr.set_z(not result.any(True))
                    processor.registers.cpsr.set_c(carry)
                    processor.registers.cpsr.set_v(overflow)
