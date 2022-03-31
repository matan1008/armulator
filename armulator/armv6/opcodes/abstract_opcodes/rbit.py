from armulator.armv6.bits_ops import set_bit_at, bit_at
from armulator.armv6.opcodes.opcode import Opcode


class Rbit(Opcode):
    def __init__(self, instruction, m, d):
        super().__init__(instruction)
        self.m = m
        self.d = d

    def execute(self, processor):
        if processor.condition_passed():
            result = 0
            m = processor.registers.get(self.m)
            for i in range(32):
                result = set_bit_at(result, 31 - i, bit_at(m, i))
            processor.registers.set(self.d, result)
