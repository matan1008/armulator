from builtins import range
from armulator.armv6.opcodes.abstract_opcode import AbstractOpcode
from bitstring import BitArray


class Rbit(AbstractOpcode):
    def __init__(self, m, d):
        super(Rbit, self).__init__()
        self.m = m
        self.d = d

    def execute(self, processor):
        if processor.condition_passed():
            result = BitArray(length=32)
            for i in range(32):
                result[i] = processor.registers.get(self.m)[31 - i]
            processor.registers.set(self.d, result)
