from armulator.opcodes.abstract_opcode import AbstractOpcode
from bitstring import BitArray


class Usub16(AbstractOpcode):
    def __init__(self, m, d, n):
        super(Usub16, self).__init__()
        self.m = m
        self.d = d
        self.n = n

    def execute(self, processor):
        if processor.condition_passed():
            diff1 = processor.registers.get(self.n)[16:32].uint - processor.registers.get(self.m)[16:32].uint
            diff2 = processor.registers.get(self.n)[0:16].uint - processor.registers.get(self.m)[0:16].uint
            processor.registers.set(self.d, BitArray(int=diff2, length=16) + BitArray(int=diff1, length=16))
            ge = "0b"
            ge += "11" if diff2 >= 0 else "00"
            ge += "11" if diff1 >= 0 else "00"
            processor.registers.cpsr.set_ge(ge)
