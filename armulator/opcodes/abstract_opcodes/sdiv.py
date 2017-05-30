from armulator.opcodes.abstract_opcode import AbstractOpcode
from bitstring import BitArray


class Sdiv(AbstractOpcode):
    def __init__(self, m, d, n):
        super(Sdiv, self).__init__()
        self.m = m
        self.d = d
        self.n = n

    def execute(self, processor):
        if processor.condition_passed():
            if processor.registers.get(self.m).int == 0:
                if processor.integer_zero_divide_trapping_enabled():
                    processor.generate_integer_zero_divide()
                else:
                    result = 0
            else:
                result = int(
                        float(processor.registers.get(self.n).int) / float(
                            processor.registers.get(self.m).int))
            processor.registers.set(self.d, BitArray(int=result, length=32))
