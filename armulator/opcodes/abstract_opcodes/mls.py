from armulator.opcodes.abstract_opcode import AbstractOpcode
from bitstring import BitArray


class Mls(AbstractOpcode):
    def __init__(self, m, a, d, n):
        super(Mls, self).__init__()
        self.m = m
        self.a = a
        self.d = d
        self.n = n

    def execute(self, processor):
        if processor.condition_passed():
            operand1 = processor.registers.get(self.n).int
            operand2 = processor.registers.get(self.m).int
            addend = processor.registers.get(self.a).int
            result = addend - operand2 * operand1
            processor.registers.set(self.d, BitArray(int=result, length=64)[-32:])
