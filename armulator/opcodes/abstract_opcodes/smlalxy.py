from armulator.opcodes.abstract_opcode import AbstractOpcode
from bitstring import BitArray


class Smlalxy(AbstractOpcode):
    def __init__(self, m_high, n_high, m, d_hi, d_lo, n):
        super(Smlalxy, self).__init__()
        self.m_high = m_high
        self.n_high = n_high
        self.m = m
        self.d_hi = d_hi
        self.d_lo = d_lo
        self.n = n

    def execute(self, processor):
        if processor.condition_passed():
            operand1 = processor.core_registers.get(self.n)[0:16] if self.n_high else processor.core_registers.get(
                    self.n)[16:]
            operand2 = processor.core_registers.get(self.m)[0:16] if self.m_high else processor.core_registers.get(
                    self.m)[16:]
            d_total = (processor.core_registers.get(self.d_hi) + processor.core_registers.get(self.d_lo)).int
            result = operand1.int * operand2.int + d_total
            processor.core_registers.set(self.d_hi, BitArray(int=result, length=64)[0:32])
            processor.core_registers.set(self.d_lo, BitArray(int=result, length=64)[32:64])
