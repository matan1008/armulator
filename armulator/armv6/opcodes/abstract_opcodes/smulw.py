from armulator.armv6.bits_ops import to_unsigned, substring, to_signed
from armulator.armv6.opcodes.opcode import Opcode


class Smulw(Opcode):
    def __init__(self, instruction, m_high, m, d, n):
        super().__init__(instruction)
        self.m_high = m_high
        self.m = m
        self.d = d
        self.n = n

    def execute(self, processor):
        if processor.condition_passed():
            m = processor.registers.get(self.m)
            operand2 = substring(m, 31, 16) if self.m_high else substring(m, 15, 0)
            result = to_signed(processor.registers.get(self.n), 32) * to_signed(operand2, 16)
            output = substring(to_unsigned(result, 48), 47, 16)
            processor.registers.set(self.d, output)
