from armulator.armv6.bits_ops import signed_sat_q, to_signed, to_unsigned
from armulator.armv6.opcodes.opcode import Opcode
from armulator.armv6.shift import shift


class Ssat(Opcode):
    def __init__(self, instruction, saturate_to, d, n, shift_t, shift_n):
        super().__init__(instruction)
        self.saturate_to = saturate_to
        self.d = d
        self.n = n
        self.shift_t = shift_t
        self.shift_n = shift_n

    def execute(self, processor):
        if processor.condition_passed():
            operand = shift(processor.registers.get(self.n), 32, self.shift_t, self.shift_n,
                            processor.registers.cpsr.c)
            result, sat = signed_sat_q(to_signed(operand, 32), self.saturate_to)
            processor.registers.set(self.d, to_unsigned(result, 32))
            if sat:
                processor.registers.cpsr.q = 1
