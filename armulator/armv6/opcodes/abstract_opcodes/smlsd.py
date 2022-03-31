from armulator.armv6.bits_ops import to_signed, substring, to_unsigned
from armulator.armv6.opcodes.opcode import Opcode
from armulator.armv6.shift import ror


class Smlsd(Opcode):
    def __init__(self, instruction, m_swap, m, a, d, n):
        super().__init__(instruction)
        self.m_swap = m_swap
        self.m = m
        self.a = a
        self.d = d
        self.n = n

    def execute(self, processor):
        if processor.condition_passed():
            operand2 = ror(processor.registers.get(self.m), 32, 16) if self.m_swap else processor.registers.get(self.m)
            n = processor.registers.get(self.n)
            product1 = to_signed(substring(n, 15, 0), 16) * to_signed(substring(operand2, 15, 0), 16)
            product2 = to_signed(substring(n, 31, 16), 16) * to_signed(substring(operand2, 31, 16), 16)
            result = product1 - product2 + to_signed(processor.registers.get(self.a), 32)
            processor.registers.set(self.d, to_unsigned(result, 32))
            if result != to_signed(to_unsigned(result, 32), 32):
                processor.registers.cpsr.q = 1
