from armulator.armv6.bits_ops import lower_chunk
from armulator.armv6.opcodes.opcode import Opcode


class Udiv(Opcode):
    def __init__(self, instruction, m, d, n):
        super().__init__(instruction)
        self.m = m
        self.d = d
        self.n = n

    def execute(self, processor):
        if processor.condition_passed():
            if processor.registers.get(self.m) == 0:
                if processor.integer_zero_divide_trapping_enabled():
                    processor.generate_integer_zero_divide()
                else:
                    result = 0
            else:
                result = int(processor.registers.get(self.n) / processor.registers.get(self.m))
            processor.registers.set(self.d, lower_chunk(result, 32))
