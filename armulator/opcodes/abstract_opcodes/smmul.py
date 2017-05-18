from armulator.opcodes.abstract_opcode import AbstractOpcode
from bitstring import BitArray


class Smmul(AbstractOpcode):
    def __init__(self, round_, m, d, n):
        super(Smmul, self).__init__()
        self.round = round_
        self.m = m
        self.d = d
        self.n = n

    def execute(self, processor):
        if processor.condition_passed():
            result = processor.core_registers.get(self.n).int * processor.core_registers.get(self.m).int
            if self.round:
                result += 0x80000000
            processor.core_registers.set(self.d, BitArray(int=result, length=64)[0:32])
