from armulator.armv6.bits_ops import to_signed, to_unsigned, substring
from armulator.armv6.opcodes.opcode import Opcode


class Smul(Opcode):
    def __init__(self, instruction, m_high, n_high, m, d, n):
        super().__init__(instruction)
        self.m_high = m_high
        self.n_high = n_high
        self.m = m
        self.d = d
        self.n = n

    def execute(self, processor):
        if processor.condition_passed():
            n = processor.registers.get(self.n)
            operand1 = substring(n, 31, 16) if self.n_high else substring(n, 15, 0)
            m = processor.registers.get(self.m)
            operand2 = substring(m, 31, 16) if self.m_high else substring(m, 15, 0)
            result = to_signed(operand1, 16) * to_signed(operand2, 16)
            processor.registers.set(self.d, to_unsigned(result, 32))
