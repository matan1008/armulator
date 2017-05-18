from armulator.opcodes.abstract_opcode import AbstractOpcode
from bitstring import BitArray
from armulator.bits_ops import count_leading_zero_bits


class Clz(AbstractOpcode):
    def __init__(self, m, d):
        super(Clz, self).__init__()
        self.m = m
        self.d = d

    def execute(self, processor):
        if processor.condition_passed():
            processor.core_registers.set(self.d, BitArray(
                    uint=count_leading_zero_bits(processor.core_registers.get(self.m)), length=32))
