from armulator.armv6.bits_ops import substring, bit_at
from armulator.armv6.configurations import arch_version
from armulator.armv6.opcodes.opcode import Opcode


class Umull(Opcode):
    def __init__(self, instruction, setflags, m, d_hi, d_lo, n):
        super().__init__(instruction)
        self.setflags = setflags
        self.m = m
        self.d_hi = d_hi
        self.d_lo = d_lo
        self.n = n

    def execute(self, processor):
        if processor.condition_passed():
            result = processor.registers.get(self.n) * processor.registers.get(self.m)
            processor.registers.set(self.d_hi, substring(result, 63, 32))
            processor.registers.set(self.d_lo, substring(result, 31, 0))
            if self.setflags:
                processor.registers.cpsr.n = bit_at(result, 63)
                processor.registers.cpsr.z = 0 if result else 1
                if arch_version() == 4:
                    processor.registers.cpsr.c = 0  # unknown
                    processor.registers.cpsr.v = 0  # unknown
