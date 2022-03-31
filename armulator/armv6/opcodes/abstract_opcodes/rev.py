from armulator.armv6.bits_ops import substring, set_substring
from armulator.armv6.opcodes.opcode import Opcode


class Rev(Opcode):
    def __init__(self, instruction, m, d):
        super().__init__(instruction)
        self.m = m
        self.d = d

    def execute(self, processor):
        if processor.condition_passed():
            result = 0
            m = processor.registers.get(self.m)
            result = set_substring(result, 31, 24, substring(m, 7, 0))
            result = set_substring(result, 23, 16, substring(m, 15, 8))
            result = set_substring(result, 15, 8, substring(m, 23, 16))
            result = set_substring(result, 7, 0, substring(m, 31, 24))
            processor.registers.set(self.d, result)
