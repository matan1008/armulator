from armulator.opcodes.abstract_opcode import AbstractOpcode
from bitstring import BitArray


class Smul(AbstractOpcode):
    def __init__(self, m_high, n_high, m, d, n):
        super(Smul, self).__init__()
        self.m_high = m_high
        self.n_high = n_high
        self.m = m
        self.d = d
        self.n = n

    def execute(self, processor):
        if processor.condition_passed():
            operand1 = processor.core_registers.get(self.n)[0:16] if self.n_high else processor.core_registers.get(
                self.n)[16:]
            operand2 = processor.core_registers.get(self.m)[0:16] if self.m_high else processor.core_registers.get(
                self.m)[16:]
            result = operand1.int * operand2.int
            processor.core_registers.set(self.d, BitArray(int=result, length=32))
