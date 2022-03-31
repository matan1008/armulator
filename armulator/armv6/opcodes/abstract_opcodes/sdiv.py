from armulator.armv6.bits_ops import to_signed, to_unsigned
from armulator.armv6.opcodes.opcode import Opcode


class Sdiv(Opcode):
    def __init__(self, instruction, m, d, n):
        super().__init__(instruction)
        self.m = m
        self.d = d
        self.n = n

    def execute(self, processor):
        if processor.condition_passed():
            if to_signed(processor.registers.get(self.m), 32) == 0:
                if processor.integer_zero_divide_trapping_enabled():
                    processor.generate_integer_zero_divide()
                else:
                    result = 0
            else:
                result = int(
                    to_signed(processor.registers.get(self.n), 32) / to_signed(processor.registers.get(self.m), 32)
                )
            processor.registers.set(self.d, to_unsigned(result, 32))
