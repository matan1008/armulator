from armulator.opcodes.abstract_opcode import AbstractOpcode
from bitstring import BitArray


class Smmla(AbstractOpcode):
    def __init__(self, round_, m, a, d, n):
        super(Smmla, self).__init__()
        self.round = round_
        self.m = m
        self.a = a
        self.d = d
        self.n = n

    def execute(self, processor):
        if processor.condition_passed():
            result = (processor.registers.get(self.a).int << 32) + processor.registers.get(
                self.n).int * processor.registers.get(self.m).int
            if self.round:
                result += 0x80000000
            processor.registers.set(self.d, BitArray(int=result, length=64)[0:32])
