from armulator.armv6.opcodes.abstract_opcode import AbstractOpcode
from armulator.armv6.shift import shift
from armulator.armv6.bits_ops import add_with_carry


class AddRegisterArm(AbstractOpcode):
    def __init__(self, setflags, m, d, n, shift_t, shift_n):
        super(AddRegisterArm, self).__init__()
        self.setflags = setflags
        self.m = m
        self.d = d
        self.n = n
        self.shift_t = shift_t
        self.shift_n = shift_n

    def execute(self, processor):
        if processor.condition_passed():
            shifted = shift(processor.registers.get(self.m), self.shift_t, self.shift_n,
                            processor.registers.cpsr.get_c())
            result, carry, overflow = add_with_carry(processor.registers.get(self.n), shifted, "0")
            if self.d == 15:
                processor.alu_write_pc(result)
            else:
                processor.registers.set(self.d, result)
                if self.setflags:
                    processor.registers.cpsr.set_n(result[0])
                    processor.registers.cpsr.set_z(not result.any(True))
                    processor.registers.cpsr.set_c(carry)
                    processor.registers.cpsr.set_v(overflow)
