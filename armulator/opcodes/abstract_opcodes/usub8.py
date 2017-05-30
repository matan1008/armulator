from armulator.opcodes.abstract_opcode import AbstractOpcode
from bitstring import BitArray


class Usub8(AbstractOpcode):
    def __init__(self, m, d, n):
        super(Usub8, self).__init__()
        self.m = m
        self.d = d
        self.n = n

    def execute(self, processor):
        if processor.condition_passed():
            diff1 = processor.registers.get(self.n)[24:32].uint - processor.registers.get(self.m)[24:32].uint
            diff2 = processor.registers.get(self.n)[16:24].uint - processor.registers.get(self.m)[16:24].uint
            diff3 = processor.registers.get(self.n)[8:16].uint - processor.registers.get(self.m)[8:16].uint
            diff4 = processor.registers.get(self.n)[0:8].uint - processor.registers.get(self.m)[0:8].uint
            processor.registers.set(self.d,
                                         BitArray(int=diff4, length=8) + BitArray(int=diff3, length=8) + BitArray(
                                             int=diff2, length=8) + BitArray(int=diff1, length=8))
            ge = "0b"
            ge += "1" if diff4 >= 0 else "0"
            ge += "1" if diff3 >= 0 else "0"
            ge += "1" if diff2 >= 0 else "0"
            ge += "1" if diff1 >= 0 else "0"
            processor.registers.cpsr.set_ge(ge)
