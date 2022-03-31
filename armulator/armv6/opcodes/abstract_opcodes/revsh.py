from armulator.armv6.bits_ops import sign_extend, lower_chunk, substring, set_substring
from armulator.armv6.opcodes.opcode import Opcode


class Revsh(Opcode):
    def __init__(self, instruction, m, d):
        super().__init__(instruction)
        self.m = m
        self.d = d

    def execute(self, processor):
        if processor.condition_passed():
            m = processor.registers.get(self.m)
            result = set_substring(0, 31, 8, sign_extend(lower_chunk(m, 8), 8, 24))
            result = set_substring(result, 7, 0, substring(m, 15, 8))
            processor.registers.set(self.d, result)
