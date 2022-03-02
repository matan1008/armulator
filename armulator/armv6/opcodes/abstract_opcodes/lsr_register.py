from armulator.armv6.bits_ops import substring, bit_at
from armulator.armv6.opcodes.opcode import Opcode
from armulator.armv6.shift import shift_c, SRType


class LsrRegister(Opcode):
    def __init__(self, instruction, setflags, m, d, n):
        super().__init__(instruction)
        self.setflags = setflags
        self.m = m
        self.d = d
        self.n = n

    def execute(self, processor):
        shift_n = substring(processor.registers.get(self.m), 7, 0)
        result, carry = shift_c(processor.registers.get(self.n), 32, SRType.LSR, shift_n, processor.registers.cpsr.c)
        processor.registers.set(self.d, result)
        if self.setflags:
            processor.registers.cpsr.n = bit_at(result, 31)
            processor.registers.cpsr.z = 0 if result else 1
            processor.registers.cpsr.c = carry
