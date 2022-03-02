from armulator.armv6.bits_ops import signed_sat_q, substring, to_signed, chain, to_unsigned
from armulator.armv6.opcodes.opcode import Opcode


class Ssat16(Opcode):
    def __init__(self, instruction, saturate_to, d, n):
        super().__init__(instruction)
        self.saturate_to = saturate_to
        self.d = d
        self.n = n

    def execute(self, processor):
        if processor.condition_passed():
            n = processor.registers.get(self.n)
            result1, sat1 = signed_sat_q(to_signed(substring(n, 15, 0), 16), self.saturate_to)
            result2, sat2 = signed_sat_q(to_signed(substring(n, 31, 16), 16), self.saturate_to)
            processor.registers.set(self.d, chain(to_unsigned(result2, 16), to_unsigned(result1, 16), 16))
            if sat1 or sat2:
                processor.registers.cpsr.q = 1
