from armulator.armv6.opcodes.abstract_opcode import AbstractOpcode
from bitstring import BitArray


class Smulw(AbstractOpcode):
    def __init__(self, m_high, m, d, n):
        super(Smulw, self).__init__()
        self.m_high = m_high
        self.m = m
        self.d = d
        self.n = n

    def execute(self, processor):
        if processor.condition_passed():
            operand2 = processor.registers.get(self.m)[0:16] if self.m_high else processor.registers.get(
                self.m)[16:]
            product = processor.registers.get(self.n).int * operand2.int
            processor.registers.set(self.d, BitArray(int=product, length=48)[0:32])
