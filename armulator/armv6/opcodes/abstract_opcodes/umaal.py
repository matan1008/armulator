from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.opcode import Opcode


class Umaal(Opcode):
    def __init__(self, instruction, m, d_hi, d_lo, n):
        super().__init__(instruction)
        self.m = m
        self.d_hi = d_hi
        self.d_lo = d_lo
        self.n = n

    def execute(self, processor):
        if processor.condition_passed():
            result = (processor.registers.get(self.n) * processor.registers.get(self.m) +
                      processor.registers.get(self.d_hi) + processor.registers.get(self.d_lo))
            processor.registers.set(self.d_hi, substring(result, 63, 32))
            processor.registers.set(self.d_lo, substring(result, 31, 0))
