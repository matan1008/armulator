from armulator.opcodes.abstract_opcode import AbstractOpcode
from bitstring import BitArray


class Umaal(AbstractOpcode):
    def __init__(self, m, d_hi, d_lo, n):
        super(Umaal, self).__init__()
        self.m = m
        self.d_hi = d_hi
        self.d_lo = d_lo
        self.n = n

    def execute(self, processor):
        if processor.condition_passed():
            result = processor.core_registers.get(self.n).uint * processor.core_registers.get(
                self.m).uint + processor.core_registers.get(
                    self.d_hi).uint + processor.core_registers.get(self.d_lo).uint
            processor.core_registers.set(self.d_hi, BitArray(uint=result, length=64)[0:32])
            processor.core_registers.set(self.d_lo, BitArray(uint=result, length=64)[32:64])
