from armulator.opcodes.abstract_opcode import AbstractOpcode
from armulator.shift import ror
from bitstring import BitArray


class Smusd(AbstractOpcode):
    def __init__(self, m_swap, m, d, n):
        super(Smusd, self).__init__()
        self.m_swap = m_swap
        self.m = m
        self.d = d
        self.n = n

    def execute(self, processor):
        if processor.condition_passed():
            operand2 = ror(processor.core_registers.get(self.m), 16) if self.m_swap else processor.core_registers.get(
                self.m)
            product1 = processor.core_registers.get(self.n)[16:32].int * operand2[16:32].int
            product2 = processor.core_registers.get(self.n)[0:16].int * operand2[0:16].int
            result = product1 - product2
            processor.core_registers.set(self.d, BitArray(int=result, length=33)[1:33])
