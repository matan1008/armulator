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
        shift_n = processor.core_registers.get(self.s)[24:32].uint
        shifted = shift(processor.core_registers.get(self.m), self.shift_t, shift_n,
                        processor.core_registers.cpsr.get_c())
        result, carry, overflow = add_with_carry(processor.core_registers.get(self.n), ~shifted, "1")
        processor.core_registers.cpsr.set_n(result[0])
        processor.core_registers.cpsr.set_z(not result.any(True))
        processor.core_registers.cpsr.set_c(carry)
        processor.core_registers.cpsr.set_v(overflow)
