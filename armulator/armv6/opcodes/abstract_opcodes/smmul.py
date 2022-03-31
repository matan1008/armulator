from armulator.armv6.bits_ops import to_signed, substring, to_unsigned
from armulator.armv6.opcodes.opcode import Opcode


class Smmul(Opcode):
    def __init__(self, instruction, round_, m, d, n):
        super().__init__(instruction)
        self.round = round_
        self.m = m
        self.d = d
        self.n = n

    def execute(self, processor):
        if processor.condition_passed():

            result = to_signed(processor.registers.get(self.n), 32) * to_signed(processor.registers.get(self.m), 32)
            if self.round:
                result += 0x80000000
            processor.registers.set(self.d, substring(to_unsigned(result, 64), 63, 32))
