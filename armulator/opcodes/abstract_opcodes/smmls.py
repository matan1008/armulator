from armulator.opcodes.abstract_opcode import AbstractOpcode
from bitstring import BitArray


class Smmls(AbstractOpcode):
    def __init__(self, round_, m, a, d, n):
        super(Smmls, self).__init__()
        self.round = round_
        self.m = m
        self.a = a
        self.d = d
        self.n = n

    def execute(self, processor):
        if processor.condition_passed():
            result = (processor.core_registers.get(self.a).int << 32) - processor.core_registers.get(
                self.n).int * processor.core_registers.get(self.m).int
            if self.round:
                result += 0x80000000
            processor.core_registers.set(self.d, BitArray(int=result, length=64)[0:32])
