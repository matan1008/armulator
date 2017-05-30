from armulator.opcodes.abstract_opcode import AbstractOpcode
from armulator.shift import shift
from armulator.bits_ops import add_with_carry


class CmpRegisterShiftedRegister(AbstractOpcode):
    def __init__(self, m, s, n, shift_t):
        super(CmpRegisterShiftedRegister, self).__init__()
        self.m = m
        self.s = s
        self.n = n
        self.shift_t = shift_t

    def execute(self, processor):
        shift_n = processor.registers.get(self.s)[24:32].uint
        shifted = shift(processor.registers.get(self.m), self.shift_t, shift_n,
                        processor.registers.cpsr.get_c())
        result, carry, overflow = add_with_carry(processor.registers.get(self.n), ~shifted, "1")
        processor.registers.cpsr.set_n(result[0])
        processor.registers.cpsr.set_z(not result.any(True))
        processor.registers.cpsr.set_c(carry)
        processor.registers.cpsr.set_v(overflow)
