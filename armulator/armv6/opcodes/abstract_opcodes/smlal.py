from armulator.armv6.bits_ops import to_signed, set_substring, to_unsigned, substring, bit_at
from armulator.armv6.configurations import arch_version
from armulator.armv6.opcodes.opcode import Opcode


class Smlal(Opcode):
    def __init__(self, instruction, setflags, m, d_hi, d_lo, n):
        super().__init__(instruction)
        self.setflags = setflags
        self.m = m
        self.d_hi = d_hi
        self.d_lo = d_lo
        self.n = n

    def execute(self, processor):
        if processor.condition_passed():
            a = to_signed(
                set_substring(processor.registers.get(self.d_lo), 63, 32, processor.registers.get(self.d_hi)), 64
            )
            result = to_signed(processor.registers.get(self.n), 32) * to_signed(processor.registers.get(self.m), 32) + a
            f_result = to_unsigned(result, 64)
            processor.registers.set(self.d_hi, substring(f_result, 63, 32))
            processor.registers.set(self.d_lo, substring(f_result, 31, 0))
            if self.setflags:
                processor.registers.cpsr.n = bit_at(f_result, 63)
                processor.registers.cpsr.z = 0 if f_result else 1
                if arch_version() == 4:
                    processor.registers.cpsr.c = 0  # unknown
                    processor.registers.cpsr.v = 0  # unknown
