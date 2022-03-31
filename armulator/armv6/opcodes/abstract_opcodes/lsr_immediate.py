from armulator.armv6.bits_ops import bit_at
from armulator.armv6.opcodes.opcode import Opcode
from armulator.armv6.shift import shift_c, SRType


class LsrImmediate(Opcode):
    def __init__(self, instruction, setflags, m, d, shift_n):
        super().__init__(instruction)
        self.setflags = setflags
        self.m = m
        self.d = d
        self.shift_n = shift_n

    def execute(self, processor):
        if processor.condition_passed():
            result, carry = shift_c(processor.registers.get(self.m), 32, SRType.LSR, self.shift_n,
                                    processor.registers.cpsr.c)
            if self.d == 15:
                processor.alu_write_pc(result)
            else:
                processor.registers.set(self.d, result)
                if self.setflags:
                    processor.registers.cpsr.n = bit_at(result, 31)
                    processor.registers.cpsr.z = 0 if result else 1
                    processor.registers.cpsr.c = carry
