from armulator.armv6.bits_ops import to_signed, to_unsigned
from armulator.armv6.opcodes.opcode import Opcode


class Mls(Opcode):
    def __init__(self, instruction, m, a, d, n):
        super().__init__(instruction)
        self.m = m
        self.a = a
        self.d = d
        self.n = n

    def execute(self, processor):
        if processor.condition_passed():
            operand1 = to_signed(processor.registers.get(self.n), 32)
            operand2 = to_signed(processor.registers.get(self.m), 32)
            addend = to_signed(processor.registers.get(self.a), 32)
            result = addend - operand2 * operand1
            processor.registers.set(self.d, to_unsigned(result, 32))
