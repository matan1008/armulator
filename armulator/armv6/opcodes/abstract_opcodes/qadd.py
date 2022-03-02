from armulator.armv6.bits_ops import signed_sat_q, to_signed
from armulator.armv6.opcodes.opcode import Opcode


class Qadd(Opcode):
    def __init__(self, instruction, m, d, n):
        super().__init__(instruction)
        self.m = m
        self.d = d
        self.n = n

    def execute(self, processor):
        if processor.condition_passed():
            result, sat = signed_sat_q(
                to_signed(processor.registers.get(self.m), 32) + to_signed(processor.registers.get(self.n), 32),
                32
            )
            processor.registers.set(self.d, result)
            if sat:
                processor.registers.cpsr.q = 1
