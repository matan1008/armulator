from armulator.armv6.bits_ops import lower_chunk, bit_at
from armulator.armv6.opcodes.opcode import Opcode
from armulator.armv6.shift import shift_c


class EorRegisterShiftedRegister(Opcode):
    def __init__(self, instruction, setflags, m, s, d, n, shift_t):
        super().__init__(instruction)
        self.setflags = setflags
        self.m = m
        self.s = s
        self.d = d
        self.n = n
        self.shift_t = shift_t

    def execute(self, processor):
        shift_n = lower_chunk(processor.registers.get(self.s), 8)
        shifted, carry = shift_c(processor.registers.get(self.m), 32, self.shift_t, shift_n, processor.registers.cpsr.c)
        result = processor.registers.get(self.n) ^ shifted
        processor.registers.set(self.d, result)
        if self.setflags:
            processor.registers.cpsr.n = bit_at(result, 31)
            processor.registers.cpsr.z = 0 if result else 1
            processor.registers.cpsr.c = carry
