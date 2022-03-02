from armulator.armv6.bits_ops import to_signed, substring, to_unsigned, set_substring
from armulator.armv6.opcodes.opcode import Opcode


class Ssub16(Opcode):
    def __init__(self, instruction, m, d, n):
        super().__init__(instruction)
        self.m = m
        self.d = d
        self.n = n

    def execute(self, processor):
        if processor.condition_passed():
            n = processor.registers.get(self.n)
            m = processor.registers.get(self.m)
            diff1 = to_signed(substring(n, 15, 0), 16) - to_signed(substring(m, 15, 0), 16)
            diff2 = to_signed(substring(n, 31, 16), 16) - to_signed(substring(m, 31, 16), 16)
            d = set_substring(0, 15, 0, to_unsigned(diff1, 16))
            d = set_substring(d, 31, 16, to_unsigned(diff2, 16))
            processor.registers.set(self.d, d)
            ge = 0b11 if diff1 >= 0 else 00
            ge = set_substring(ge, 3, 2, 0b11 if diff2 >= 0 else 00)
            processor.registers.cpsr.ge = ge
