from armulator.opcodes.abstract_opcode import AbstractOpcode
from bitstring import BitArray


class Udiv(AbstractOpcode):
    def __init__(self, m, d, n):
        super(Udiv, self).__init__()
        self.m = m
        self.d = d
        self.n = n

    def execute(self, processor):
        if processor.condition_passed():
            if processor.core_registers.get(self.m).uint == 0:
                if processor.integer_zero_divide_trapping_enabled():
                    processor.generate_integer_zero_divide()
                else:
                    result = 0
            else:
                result = int(
                    float(processor.core_registers.get(self.n).uint) / float(processor.core_registers.get(self.m).uint))
            processor.core_registers.set(self.d, BitArray(int=result, length=32))
